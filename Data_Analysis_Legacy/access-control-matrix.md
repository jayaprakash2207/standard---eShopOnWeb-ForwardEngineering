# Access Control Matrix — eShopOnWeb
> Source: [Authorize] attributes, role constants, JWT configuration, seed data
> Confidence: 0.9 (code evidence)
> Extraction date: 2026-07-06

---

## Roles Defined

| Role | Constant | Description |
|------|----------|-------------|
| **Administrators** | `BlazorShared.Authorization.Constants.Roles.ADMINISTRATORS = "Administrators"` | Full catalogue management rights. Seeded account: `admin@microsoft.com`. |
| *(Authenticated User)* | ASP.NET Identity cookie auth — no named role | Any logged-in registered member. Seeded account: `demouser@microsoft.com`. |
| *(Anonymous)* | No authentication | Unauthenticated browser session. Identified by a GUID cookie for basket purposes. |

---

## Access Control Matrix — Web MVC (Cookie Authentication)

| Resource / Operation | Anonymous | Authenticated User | Administrator |
|---------------------|:---------:|:-----------------:|:-------------:|
| Browse catalog (homepage, listing) | ✅ | ✅ | ✅ |
| View product details | ✅ | ✅ | ✅ |
| Add item to basket | ✅ | ✅ | ✅ |
| View basket | ✅ | ✅ | ✅ |
| Update basket quantities | ✅ | ✅ | ✅ |
| **Checkout (place order)** | ❌ | ✅ | ✅ |
| View my orders | ❌ | ✅ | ✅ |
| View order details | ❌ | ✅ | ✅ |
| **Admin: Manage catalog items (Web MVC admin pages)** | ❌ | ❌ | ✅ |
| Account registration | ✅ | N/A | N/A |
| Account login | ✅ | N/A | N/A |
| Account management (ManageController) | ❌ | ✅ | ✅ |

**Checkout:** `[Authorize]` on `CheckoutModel` — any authenticated user (no role required).
**Admin pages:** `[Authorize(Roles = "Administrators")]` on `Pages/Admin/IndexModel`.

---

## Access Control Matrix — PublicApi (JWT Bearer Authentication)

| Endpoint | HTTP Method | Anonymous | Authenticated JWT (any) | Administrator JWT |
|---------|-------------|:---------:|:-----------------------:|:-----------------:|
| GET /api/catalog-items | List paged | ✅ | ✅ | ✅ |
| GET /api/catalog-items/{id} | Get by ID | ✅ | ✅ | ✅ |
| **POST /api/catalog-items** | Create | ❌ | ❌ | ✅ |
| **PUT /api/catalog-items** | Update | ❌ | ❌ | ✅ |
| **DELETE /api/catalog-items/{id}** | Delete | ❌ | ❌ | ✅ |
| GET /api/catalog-brands | List brands | ✅ | ✅ | ✅ |
| GET /api/catalog-types | List types | ✅ | ✅ | ✅ |
| POST /api/authenticate | Get JWT token | ✅ | N/A | N/A |
| GET /User | Current user info (BlazorAdmin auth check) | ✅ (returns anonymous) | ✅ | ✅ |

**Write endpoint authorization:** `[Authorize(Roles = "Administrators", AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]`
on `CreateCatalogItemEndpoint`, `UpdateCatalogItemEndpoint`, `DeleteCatalogItemEndpoint`.

---

## Access Control Matrix — BlazorAdmin (WASM + JWT)

| Operation | Anonymous | Authenticated JWT (no role) | Administrator JWT |
|-----------|:---------:|:---------------------------:|:-----------------:|
| View admin UI | ✅ (redirected to login page) | ❌ | ✅ |
| List catalog items | ❌ | ❌ | ✅ |
| View catalog item details | ❌ | ❌ | ✅ |
| **Create catalog item** | ❌ | ❌ | ✅ |
| **Edit catalog item** | ❌ | ❌ | ✅ |
| **Delete catalog item** | ❌ | ❌ | ✅ |

**Client-side enforcement:** `CustomAuthStateProvider` + Blazor `[Authorize]` component attributes.
**Server-side enforcement:** JWT `[Authorize(Roles = "Administrators")]` on all write endpoints in PublicApi (defence in depth — both layers enforce the same rule).

---

## Authentication Mechanisms

| Mechanism | Used By | Token Type | TTL / Expiry |
|-----------|---------|------------|-------------|
| ASP.NET Core Cookie Auth | Web MVC (shoppers) | Encrypted server-issued cookie | Configured in Web startup (ConfigureCookieSettings) |
| JWT Bearer (HS256) | PublicApi ↔ BlazorAdmin | JWT signed with `AuthorizationConstants.JWT_SECRET_KEY` | Not explicitly set — JWT default |
| Anonymous basket cookie | Web MVC guests | GUID in cookie | **10 years** |
| BlazorAdmin auth state cache | BlazorAdmin in-memory | ClaimsPrincipal cached in provider | **60 seconds** (hardcoded `UserCacheRefreshInterval`) |

---

## Seeded Accounts

| Username | Role | Password | Source |
|----------|------|----------|--------|
| demouser@microsoft.com | (none) | Pass@word1 | `AppIdentityDbContextSeed.SeedAsync` |
| admin@microsoft.com | Administrators | Pass@word1 | `AppIdentityDbContextSeed.SeedAsync` |

⚠️ Both passwords use `AuthorizationConstants.DEFAULT_PASSWORD` — hardcoded in source code with TODO: "Don't use this in production".

---

## Governance and Security Notes

1. **JWT secret key is hardcoded** in `AuthorizationConstants.JWT_SECRET_KEY` ("SecretKeyOfDoomThatMustBeAMinimumNumberOfBytes") with a TODO to move to an environment variable. A leaked key allows any party to forge admin JWT tokens.

2. **No JWT token revocation.** Tokens cannot be invalidated before natural expiry. If an admin account is compromised, the token remains valid.

3. **BlazorAdmin auth cache (60 seconds).** Role revocations take up to 60 seconds to take effect in the admin UI. Hardcoded — TODO comment: "Get Default Cache Duration from Config".

4. **JWT Issuer/Audience validation disabled** (`ValidateIssuer = false`, `ValidateAudience = false`) — any token signed with the known secret is accepted regardless of origin.

5. **Admin catalogue management flows through two layers:** BlazorAdmin enforces role client-side, and PublicApi enforces it server-side via JWT. The Web MVC `/Admin` pages also require the Administrators role but these are read-only views that link to BlazorAdmin.
