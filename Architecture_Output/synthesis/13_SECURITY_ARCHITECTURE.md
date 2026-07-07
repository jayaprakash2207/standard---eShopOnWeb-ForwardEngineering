=== DOCUMENT: 13_SECURITY_ARCHITECTURE.md ===

# Security Architecture — eShopOnWeb
## RBAC Model, Threat Assessment, and Modernization Plan

---

## 1. CRITICAL SECURITY ALERT

The following items block any production deployment:

| Priority | Issue | Location | Impact |
|----------|-------|----------|--------|
| P0 | JWT_SECRET_KEY = "SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes" hardcoded in source | AuthorizationConstants.cs:10 | Anyone with repo access can forge valid admin JWT tokens |
| P0 | DEFAULT_PASSWORD = "Pass@word1" seeded to admin@microsoft.com on every startup | AppIdentityDbContextSeed.cs:21,25 | Admin account compromised on every fresh deployment |
| P0 | JWT ValidateIssuer=false, ValidateAudience=false | PublicApi/Program.cs:65-66 | Tokens from any source accepted; no issuer binding |

---

## 2. Authentication Architecture

### Web Application (Cookie-based)

```
Customer Browser
    │
    │  POST /Account/Login {email, password}
    ▼
SignInManager.PasswordSignInAsync(
    username, password,
    isPersistent: false,      ← no persistent cookie
    lockoutOnFailure: false   ← web login does NOT enforce lockout
)
    │
    ├── Success ─► Set-Cookie: EshopIdentifier=<encrypted-ticket>
    │              HttpOnly: true
    │              Secure: true (SecurePolicy=Always)
    │              SameSite: Lax
    │              Expires: +60 minutes (ValidityMinutesPeriod)
    │
    └── Failure ─► Return login page with error
```

**Cookie revocation mechanism:**
```csharp
// On logout (UserController.Logout):
_cache.Set($"{userId}:{identityKey}", true,
    absoluteExpiry: DateTime.Now.AddMinutes(ValidityMinutesPeriod));
// RevokeAuthenticationEvents checks this cache on every authenticated request
```

### API Authentication (JWT Bearer)

```
Admin Client (BlazorAdmin)
    │
    │  POST /api/authenticate {username, password}
    ▼
AuthenticateEndpoint
    │
    SignInManager.PasswordSignInAsync(
        username, password,
        isPersistent: false,
        lockoutOnFailure: true   ← API login enforces lockout (BR-30)
    )
    │
    ├── Success ─► IdentityTokenClaimService.GetTokenAsync(username)
    │                 ├── GetRolesAsync(user) ──► IdentityDB
    │                 ├── new JwtSecurityToken {
    │                 │     subject: username,
    │                 │     claims: [role claims],
    │                 │     expires: now + 7 days,
    │                 │     signingCredentials: HMAC-SHA256(JWT_SECRET_KEY)
    │                 │   }
    │                 └── Return token string
    │
    └── Failure ─► IsLockedOut/IsNotAllowed/RequiresTwoFactor response
```

### BlazorAdmin Auth Relay

```
BlazorAdmin (browser WASM)
    │
    │  Every 60 seconds: GET /User (Web endpoint)
    ▼
UserController.GetCurrentUser()
    ├── Returns UserInfo { IsAuthenticated, Token, Claims }
    └── Token = JWT obtained at last full authentication
    │
BlazorAdmin attaches token:
    HttpClient.DefaultRequestHeaders.Authorization = "Bearer {token}"
    └── All PublicApi calls carry this header
```

---

## 3. RBAC Model

### Roles

| Role | ID | Source | Seeded? | Members |
|------|----|--------|---------|---------|
| Administrators | IdentityDB: AspNetRoles | AppIdentityDbContextSeed | ✅ Yes | admin@microsoft.com |
| (implicit) Buyers | None (no role entity) | Convention (email = BuyerId) | N/A | All registered users |

### Permission Matrix

| Action | Anonymous | Registered Customer | Administrator |
|--------|-----------|--------------------|-|
| Browse product catalog | ✅ | ✅ | ✅ |
| View product detail | ✅ | ✅ | ✅ |
| Manage anonymous basket | ✅ | ✅ | ✅ |
| Manage authenticated basket | ❌ | ✅ | ✅ |
| Place order | ❌ | ✅ | ✅ |
| View own order history | ❌ | ✅ | ✅ |
| Register account | ✅ | N/A | N/A |
| Login | ✅ | N/A | N/A |
| **Create catalog item** | ❌ | ❌ | ✅ (JWT) |
| **Update catalog item** | ❌ | ❌ | ✅ (JWT) |
| **Delete catalog item** | ❌ | ❌ | ✅ (JWT) |
| Authenticate via API | ✅ | ✅ | ✅ |

### RBAC Enforcement Points

| Endpoint / Page | Mechanism | Attribute |
|----------------|-----------|-----------|
| POST /api/catalog-items | JWT Bearer | `[Authorize(Roles="Administrators", AuthenticationSchemes=JwtBearerDefaults)]` |
| PUT /api/catalog-items | JWT Bearer | Same |
| DELETE /api/catalog-items/{id} | JWT Bearer | Same |
| Web Checkout page | Cookie session | `[Authorize]` (any authenticated user) |
| Web Order History | Cookie session | `[Authorize]` (ASSUMED) |
| GET /api/* (catalog reads) | None | Anonymous — by design |

---

## 4. Secrets Management

### Current State (by Environment)

| Secret | Development | Docker | Production | Risk |
|--------|-------------|--------|------------|------|
| JWT_SECRET_KEY | Hardcoded in source | Hardcoded in source | Hardcoded in source | **CRITICAL** |
| DEFAULT_PASSWORD | Hardcoded in source | Hardcoded in source | Hardcoded in source | **CRITICAL** |
| AUTH_KEY | Hardcoded in source | Hardcoded in source | Hardcoded in source | HIGH |
| SQL catalog connection | User Secrets | docker-compose env var | Key Vault ✅ | OK (prod) |
| SQL identity connection | User Secrets | docker-compose env var | Key Vault ✅ | OK (prod) |
| SQL SA_PASSWORD | N/A | Hardcoded docker-compose | Azure Key Vault ✅ | OK (prod) |

### Recommended Secrets Architecture

```
Azure Key Vault
    ├── Secrets:
    │   ├── jwt-signing-key          (256-bit random, Base64)
    │   ├── catalog-connection-string
    │   ├── identity-connection-string
    │   ├── sql-admin-password       (already wired)
    │   └── app-user-password        (already wired)
    │
    └── Access:
        ├── Web App Service (SystemAssigned Managed Identity) → get+list
        └── PublicApi App Service (after TD-12 resolved) → get+list

Development:
    └── dotnet user-secrets set "Jwt:SigningKey" "<local-dev-key>"
        (per-developer; never committed to source)
```

---

## 5. Network Security

### TLS Configuration

| Component | Min TLS | HTTPS Enforced | FTPS |
|-----------|---------|---------------|------|
| Azure App Service | 1.2 | ✅ httpsOnly | FtpsOnly |
| Azure SQL (catalog) | 1.2 | N/A (TCP) | N/A |
| Azure SQL (identity) | 1.2 | N/A (TCP) | N/A |
| Docker services | None (HTTP) | ❌ dev only | N/A |

### Firewall Configuration (CRITICAL GAP)

```
Azure SQL Firewall Rule:
    Rule Name: "AllowAllWindowsAzureIps" (approximation)
    Start IP: 0.0.0.1
    End IP:   255.255.255.254
    ← ALL internet IPs allowed to connect to SQL Server

Recommended fix:
    Option A: Azure Service Endpoint (VNet integration)
        └── Only App Service subnet can reach SQL
    Option B: Private Endpoint
        └── SQL accessible only from private VNet
    Option C: App Service Outbound IP whitelist
        └── Restrict to known outbound IPs (App Service → Properties → Outbound IPs)
```

### CORS Configuration

| Surface | Allowed Origins | Risk |
|---------|----------------|------|
| Web appsettings.json | AllowedHosts: * | All hosts permitted |
| PublicApi appsettings.json | AllowedHosts: * | All hosts permitted |
| Azure App Service | portal.azure.com, ms.portal.azure.com + param | Acceptable |

---

## 6. PII and Data Protection

| Data | Location | Classification | Current Protection |
|------|----------|---------------|-------------------|
| Email (BuyerId) | CatalogDB: Baskets, Orders | PII | SQL Server TDE (Azure SQL default) |
| Shipping address | CatalogDB: Orders | PII — physical location | SQL Server TDE |
| Email, PasswordHash | IdentityDB: AspNetUsers | PII + Sensitive | SQL Server TDE; PBKDF2 hash |
| JWT token | Browser memory + Set-Cookie (Web /User endpoint relays) | Sensitive | HTTPS in transit |
| Anonymous basket GUID | Browser cookie | Session identifier | No HttpOnly flag ← gap |

**GDPR / Data Minimisation Notes:**
- BuyerId in Baskets/Orders stores email; this links PII to purchase history
- No user data deletion mechanism exists in current implementation
- Anonymous basket GUIDs are retained indefinitely (no expiry)

---

## 7. Security Modernization Plan

### Phase 1 — Pre-Production Blockers (Must complete before any deployment)

| Action | Target | Effort |
|--------|--------|--------|
| Rotate JWT_SECRET_KEY; store in Key Vault | AuthorizationConstants.cs | 1 day |
| Remove DEFAULT_PASSWORD from source; use Key Vault random password | AppIdentityDbContextSeed.cs | 1 day |
| Add ValidateIssuer=true, ValidateAudience=true | PublicApi/Program.cs | 2 hours |
| Add RequireHttpsMetadata=true | PublicApi/Program.cs | 1 hour |
| Fix [Authorize]+[AllowAnonymous] conflict on UserController | UserController.cs | 30 min |
| Add secret scanning to CI pipeline (gitleaks/trufflehog) | .github/workflows/ | 2 hours |

### Phase 2 — High Priority (Complete within first sprint post-launch)

| Action | Target | Effort |
|--------|--------|--------|
| Restrict Azure SQL firewall to App Service outbound IPs or Private Endpoint | sqlserver.bicep | 1 day |
| Remove exception.Message from 500 responses | ExceptionMiddleware.cs | 30 min |
| Add HttpOnly flag to anonymous basket cookie | Checkout.cshtml.cs | 30 min |
| Set AllowedHosts to specific domain | appsettings.json | 30 min |
| Add CORS policy restricting origins explicitly | Program.cs (both services) | 2 hours |

### Phase 3 — Security Hardening

| Action | Target | Effort |
|--------|--------|--------|
| Introduce granular RBAC (e.g., CatalogEditor, CatalogViewer) | Program.cs, endpoints | 1 week |
| Add rate limiting on /api/authenticate and all PublicApi endpoints | Program.cs middleware | 1 day |
| Implement Content Security Policy headers | Web/Program.cs | 1 day |
| Add security headers (X-Content-Type-Options, X-Frame-Options, HSTS) | Middleware | 1 day |
| Implement GDPR user data deletion endpoint | IdentityController | 1 week |
| Add SQL injection protection audit (EF Core parameterizes — verify no raw SQL) | All Specifications | 1 day |
| Move to SameSite=Strict for auth cookie (test cross-origin flows) | ConfigureCookieSettings.cs | 2 hours |
