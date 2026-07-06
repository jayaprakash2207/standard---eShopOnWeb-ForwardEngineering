=== DOCUMENT: 11_API_CONTRACT_SPECIFICATION.md ===

# API Contract Specification — eShopOnWeb PublicApi

**Base URL:** `http://localhost:5200` (Docker dev) | Azure: **not deployed (TD-12)**
**OpenAPI:** `/swagger/v1/swagger.json` | **Swagger UI:** `/swagger`
**API Version:** v1 (string label only; no semantic versioning)
**Auth Scheme:** `Bearer {jwt}` in Authorization header for protected endpoints

---

## Authentication

### POST /api/authenticate

**Description:** Validates credentials and issues a signed JWT token.
**Auth Required:** None
**Request Body:** `application/json`

```json
{
  "username": "admin@microsoft.com",
  "password": "Pass@word1"
}
```

**Response 200 OK:**
```json
{
  "result": true,
  "isLockedOut": false,
  "isNotAllowed": false,
  "requiresTwoFactor": false,
  "username": "admin@microsoft.com",
  "token": "<jwt-string>"
}
```

**Response 200 OK (failed login variants):**
```json
{ "result": false, "isLockedOut": true, "isNotAllowed": false, "requiresTwoFactor": false, "username": "", "token": "" }
```

**Security Notes:**
- JWT token: HMAC-SHA256, 7-day validity (NFR-03)
- `lockoutOnFailure: true` — repeated failures lock the account (BR-30)
- JWT_SECRET_KEY is hardcoded (TD-01 CRITICAL) — must be rotated before production
- ValidateIssuer=false, ValidateAudience=false (TD-03 CRITICAL)

---

## Catalog Items

### GET /api/catalog-items

**Description:** Returns a paged list of catalog items filtered by brand and/or type.
**Auth Required:** None
**⚠️ WARNING:** Includes `await Task.Delay(1000)` — every request is delayed 1 second (TD-07 — REMOVE)

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| pageIndex | int | No | 0 | Zero-based page index |
| pageSize | int | No | 10 | Items per page (0 = all) |
| brandId | int? | No | null | Filter by CatalogBrand.Id |
| typeId | int? | No | null | Filter by CatalogType.Id |

**Response 200 OK:**
```json
{
  "pageCount": 3,
  "catalogItems": [
    {
      "id": 1,
      "name": ".NET Bot Black Sweatshirt",
      "description": "...",
      "price": 19.50,
      "pictureUri": "http://catalogbaseurltobereplaced/images/products/1.png",
      "catalogTypeId": 2,
      "catalogType": "T-Shirt",
      "catalogBrandId": 2,
      "catalogBrand": "Visual Studio",
      "pictureBase64": null,
      "pictureName": null
    }
  ]
}
```

---

### GET /api/catalog-items/{catalogItemId}

**Description:** Returns a single catalog item by ID.
**Auth Required:** None

**Path Parameter:** `catalogItemId` (int)

**Response 200 OK:** Single `CatalogItemDto` (same structure as item in paged list)
**Response 404 Not Found:** Item with given ID does not exist

---

### POST /api/catalog-items

**Description:** Creates a new catalog item.
**Auth Required:** `Bearer {jwt}` — Administrators role required

**Request Body:** `application/json`
```json
{
  "catalogTypeId": 2,
  "catalogBrandId": 2,
  "name": "New Product Name",
  "description": "Product description text",
  "price": 29.99,
  "pictureUri": "images/products/new.png",
  "pictureBase64": "base64encodedimage...",
  "pictureName": "new.jpg"
}
```

**Validation Rules:**
- `name`: required, non-empty; must be unique (duplicate → 409 Conflict via ExceptionMiddleware)
- `description`: required, non-empty
- `price`: 0.01–1000.00, max 2 decimal places
- `catalogBrandId`: must be > 0 and reference an existing brand
- `catalogTypeId`: must be > 0 and reference an existing type
- `pictureBase64`: if provided, image must be JPG/PNG/GIF/JPEG format, ≤ 512 KB

**Response 201 Created:**
```json
{ "id": 42, "name": "New Product Name", ... }
```

**Response 400 Bad Request:** Validation failure
**Response 401 Unauthorized:** No valid JWT
**Response 403 Forbidden:** Valid JWT but not Administrators role
**Response 409 Conflict:** Duplicate product name

---

### PUT /api/catalog-items

**Description:** Updates an existing catalog item.
**Auth Required:** `Bearer {jwt}` — Administrators role required

**Request Body:** `application/json`
```json
{
  "id": 42,
  "catalogTypeId": 2,
  "catalogBrandId": 2,
  "name": "Updated Product Name",
  "description": "Updated description",
  "price": 34.99,
  "pictureUri": "images/products/updated.png",
  "pictureBase64": null,
  "pictureName": null
}
```

**Response 200 OK:** Updated `CatalogItemDto`
**Response 404 Not Found:** Item not found
**Response 400/401/403/409:** Same as POST

---

### DELETE /api/catalog-items/{catalogItemId}

**Description:** Permanently deletes a catalog item.
**Auth Required:** `Bearer {jwt}` — Administrators role required

**Path Parameter:** `catalogItemId` (int)

**Response 204 No Content:** Successfully deleted
**Response 404 Not Found:** Item not found
**Response 401 Unauthorized:** No valid JWT
**Response 403 Forbidden:** Not Administrators role

---

## Catalog Brands

### GET /api/catalog-brands

**Description:** Returns all catalog brands.
**Auth Required:** None

**Response 200 OK:**
```json
{
  "catalogBrands": [
    { "id": 1, "name": "Azure" },
    { "id": 2, "name": "Visual Studio" }
  ]
}
```

---

## Catalog Types

### GET /api/catalog-types

**Description:** Returns all catalog types.
**Auth Required:** None

**Response 200 OK:**
```json
{
  "catalogTypes": [
    { "id": 1, "name": "Mug" },
    { "id": 2, "name": "T-Shirt" }
  ]
}
```

---

## Error Response Format

All errors return `application/json`:

```json
{
  "statusCode": 409,
  "message": "CatalogItem with this name already exists."
}
```

**⚠️ Security Issue (TD-04):** For unhandled exceptions (500), the raw `exception.Message` is included in the `message` field. This leaks internal implementation details to clients. In production, return a generic message and log the full exception server-side.

---

## Web Internal Endpoint

### GET /User

**Description:** Returns the current user's authentication state and JWT token for BlazorAdmin consumption.
**Auth Required:** ASP.NET Identity cookie session
**Undocumented:** No OpenAPI spec; no versioning
**⚠️ Security Note (TD-10):** Both `[Authorize]` and `[AllowAnonymous]` are applied to this controller; `[AllowAnonymous]` overrides `[Authorize]` in ASP.NET Core, making this endpoint effectively public.

**Response 200 OK:**
```json
{
  "isAuthenticated": true,
  "nameClaimType": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name",
  "roleClaimType": "http://schemas.microsoft.com/ws/2008/06/identity/claims/role",
  "token": "<jwt-string>",
  "claims": [
    { "type": "name", "value": "admin@microsoft.com" },
    { "type": "role", "value": "Administrators" }
  ]
}
```

---

## JWT Token Structure

**Algorithm:** HMAC-SHA256 (`HS256`)
**Signing Key:** `AuthorizationConstants.JWT_SECRET_KEY` (**HARDCODED — CRITICAL TD-01**)
**Lifetime:** 7 days from issuance
**Claims:**

| Claim | Value |
|-------|-------|
| `sub` (or `unique_name`) | User's email/username |
| `role` | All role names (e.g., "Administrators") |
| `nbf` | Not-before timestamp |
| `exp` | Expiry = issued + 7 days |
| `iat` | Issued-at timestamp |

**Validation (PublicApi):**
- `ValidateIssuerSigningKey: true`
- `ValidateIssuer: false` ← **CRITICAL GAP (TD-03)**
- `ValidateAudience: false` ← **CRITICAL GAP (TD-03)**
- `RequireHttpsMetadata: false` ← **SECURITY GAP**

---

## CORS Configuration

| Service | Allowed Origins |
|---------|----------------|
| PublicApi | `BaseUrlConfiguration.WebBase` (configured per environment) |
| Web (Azure) | `https://portal.azure.com`, `https://ms.portal.azure.com` + param |
| Both | `AllowedHosts: *` in appsettings.json |
