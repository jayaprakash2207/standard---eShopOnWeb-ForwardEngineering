# Access Control Matrix — eShopOnWeb

`db_connection: CODE-ONLY — db_connection_results empty; no live role/permission grants checked. Roles below are derived from class/source names found in extraction (AuthorizationConstants, BlazorShared.Authorization.Constants/Roles).`

## Roles Identified

| Role | Source Evidence | Confidence |
|---|---|---|
| `"Administrators"` (CONFIRMED literal string, RC-008) | `Roles.ADMINISTRATORS = "Administrators"` (src/BlazorShared/Authorization/Constants.cs) | 0.95 |
| Authenticated user (default, no explicit role name found) | Standard ASP.NET Identity — any logged-in AspNetUsers row | 0.7 |
| Anonymous / Guest | Implicit — catalog browsing and basket creation typically allowed without login in eShopOnWeb | 0.7 |

> RESOLVED (RC-008): the literal role name is confirmed as `"Administrators"` via `src/BlazorShared/Authorization/Constants.cs`. Note `AuthorizationConstants` (src/ApplicationCore/Constants/AuthorizationConstants.cs) does **not** contain role names — it holds hardcoded auth secrets (`AUTH_KEY`, `JWT_SECRET_KEY`, `DEFAULT_PASSWORD = "Pass@word1"`), see RC-006 in pii-inventory.json. confidence 0.95.

## Access Matrix (by data domain)

| Data Domain | Anonymous | Authenticated Customer | Administrator |
|---|---|---|---|
| Catalog (browse products/brands/types) | ✅ Read | ✅ Read | ✅ Read/Write (via BlazorAdmin + PublicApi) |
| Basket (own) | ✅ Create/Read/Update (session or guest-id based) | ✅ Full CRUD on own basket | ✅ (own basket only, no special elevation expected) |
| Basket (other users') | ❌ | ❌ | UNKNOWN — confidence < 0.7, not confirmed whether admins can view other baskets |
| Orders (own) | ❌ (must authenticate to checkout) | ✅ Create + Read own orders | UNKNOWN whether admins can view all orders — INFERRED ✅ likely yes (typical admin capability), confidence 0.65 |
| Orders (all customers) | ❌ | ❌ | INFERRED ✅, confidence 0.65 — not confirmed in supplied extraction |
| Identity (AspNetUsers/Roles) | ❌ | Self only (profile/password) | INFERRED ✅ user management, confidence 0.6 — ASP.NET Identity admin UI not confirmed present |
| Payment Methods | ❌ | ❌ — RESOLVED (RC-002): Buyer/PaymentMethod confirmed not persisted (no DbSet, no repository); this row is N/A for the current schema | ❌ |
| BlazorAdmin UI (catalog management) | ❌ | ❌ | ✅ — gated via `[Authorize]` attributes referencing `Roles.ADMINISTRATORS = "Administrators"` (src/BlazorShared/Authorization/Constants.cs, CONFIRMED RC-008) |

## Authentication Mechanism
- `ITokenClaimsService` (src/ApplicationCore/Interfaces/ITokenClaimsService.cs) — issues claims, likely backing JWT bearer auth for PublicApi consumed by BlazorAdmin/mobile clients. confidence 0.7.
- `CustomAuthStateProvider` (src/BlazorAdmin/CustomAuthStateProvider.cs) — Blazor WASM client-side auth state, backed by cookie storage (`Cookies.cs`); re-validates against the server at most every 60 seconds (`UserCacheRefreshInterval`, RC-005). confidence 0.85.
- **Security note (RC-006)**: `src/ApplicationCore/Constants/AuthorizationConstants.cs` hardcodes `AUTH_KEY`, `JWT_SECRET_KEY`, and `DEFAULT_PASSWORD = "Pass@word1"` (all flagged `// TODO` as non-production). These underpin the JWT/auth mechanisms referenced above — flag for Gate G1 to confirm they're overridden outside local/demo environments.

## Gaps / Action Items
1. ~~Extract literal role name strings~~ — RESOLVED (RC-008): `"Administrators"`.
2. Confirm whether Administrators can view/modify other customers' orders or baskets (data privacy implication) — still open, requires business-intent input (Gate G1).
3. ~~Confirm whether a Payment Methods feature is live~~ — RESOLVED (RC-002): not persisted, no role/ownership restrictions apply today.

## Change Records
- **RC-008** (ENRICHED): Confirmed literal Administrators role name and clarified AuthorizationConstants.cs contents. confidence 0.75 → 0.95.
- **RC-002** (CORRECTED): Payment Methods row resolved — Buyer/PaymentMethod confirmed not persisted.
- **RC-005 / RC-006** (ADDED): CustomAuthStateProvider 60s refresh interval; hardcoded auth secrets in AuthorizationConstants.cs.
