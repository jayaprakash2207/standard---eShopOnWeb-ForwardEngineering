# Data Quality Report — eShopOnWeb

`db_connection: CODE-ONLY — db_connection_results empty in extraction; no row counts or live constraint checks available. All findings below are derived from EF entity/code structure only.`

## 1. Volume
```
"volume": "UNKNOWN",
"volume_detail": "DB not connected — db_connection_results was an empty array in the supplied extraction. No psql/sqlcmd command was recorded as attempted."
```
All tables (Catalog, CatalogBrands, CatalogTypes, Baskets, BasketItems, Orders, OrderItems, AspNetUsers, etc.): row counts UNKNOWN.

## 2. Referential Integrity Risks (code-derived)

| Issue | Severity | Confidence | Detail |
|---|---|---|---|
| `Baskets.BuyerId` / `Orders.BuyerId` are unenforced cross-database soft references to `AspNetUsers.Id` | MEDIUM | 0.8 | No FK constraint possible since CatalogDb and IdentityDb are separate databases/contexts. Orphaned baskets/orders possible if a user is deleted from IdentityDb without cleanup in CatalogDb. |
| FK delete behavior for `CatalogItem` ← `BasketItem`/`OrderItem` not visible | UNKNOWN | <0.7 | If `ON DELETE NO ACTION` (typical EF Core default for non-owned FK to avoid multiple cascade paths), deleting a `CatalogItem` referenced by an existing `BasketItem` would fail with an FK violation error. Needs migration-file or live-DB confirmation. |
| `OrderItem.ItemOrdered_CatalogItemId` is a denormalized snapshot, not an enforced FK | LOW (by design) | 0.8 | This is intentional (preserves order history even if catalog item is later deleted) — not a defect, but should be documented so engineers don't "fix" it by adding an FK. |

## 3. Nullability / Validation Gaps
- `CatalogItem.Description`, `PictureUri` — INFERRED nullable (confidence 0.75). Not confirmed.
- `Address` fields on `Orders` — all INFERRED nullable string columns via EF owned-type convention; actual `[Required]` annotations not visible in supplied extraction (confidence 0.75).
- 7 validation-category business artifacts were reported in extraction summary (`"validation": 7`) but their specific rules were not included in the entity excerpts — UNKNOWN which fields they apply to. Flagged for Phase 1 deep-read by Agent 2.

## 4. Soft-Delete / Audit Columns
- `BaseEntity` (src/ApplicationCore/Entities/BaseEntity.cs) provides only `Id` based on its one-line content summary — no `IsDeleted`, `CreatedAt`, `ModifiedAt`, or audit columns were observable in the supplied extraction.
- **Finding**: No soft-delete pattern detected anywhere in the supplied entity list. If retention/audit requirements exist, this is a gap. confidence 0.75 (absence-based, could be hidden in a partial class or interceptor not in extraction).

## 5. Shadow / Unconfirmed Entities — RESOLVED (RC-002)
- `Buyer` and `PaymentMethod` (BuyerAggregate) exist as source files but are **CONFIRMED dead/unmapped code**: `src/Infrastructure/Data/CatalogContext.cs` declares exactly 7 DbSets (Baskets, CatalogItems, CatalogBrands, CatalogTypes, Orders, OrderItems, BasketItems) and `src/Infrastructure/Identity/AppIdentityDbContext.cs`'s `OnModelCreating` only calls `base.OnModelCreating`. No `modelBuilder.Entity<Buyer>()` or `IRepository<Buyer>` usage exists anywhere in src/. confidence 0.9.

## 6. Connection String Exposure & Provider Mismatch (RC-001)
- `ConnectionStrings.CatalogConnection` and `ConnectionStrings.IdentityConnection` appear in multiple files: `src/Web/appsettings.json`, `src/Web/appsettings.Docker.json`, `src/PublicApi/appsettings.json`, `src/PublicApi/appsettings.Docker.json`.
- **CONFIRMED**: `src/Web/appsettings.json` (the config actually wired up via `UseNpgsql` in `src/Infrastructure/Dependencies.cs`) uses **PostgreSQL** connection strings (`Host=localhost;Port=5432;Database=eShopCatalog/eShopIdentity;Username=postgres;...`).
- `appsettings.Docker.json` files still contain **SQL Server**-style connection strings (`Server=sqlserver,1433;...Initial Catalog=Microsoft.eShopOnWeb.CatalogDb`). Since `Dependencies.cs` registers `UseNpgsql` unconditionally, these Docker SQL Server strings appear to be **stale leftovers from the original SQL Server template** and would not be usable as-is with the current Npgsql provider registration. This is a configuration-drift risk worth flagging for Gate G1 — confidence 0.85.

## 7. Hardcoded Secrets (RC-006)
- `src/ApplicationCore/Constants/AuthorizationConstants.cs` hardcodes `AUTH_KEY`, `JWT_SECRET_KEY` (both placeholder "...OfDoomThatMustBeAMinimumNumberOfBytes" strings), and `DEFAULT_PASSWORD = "Pass@word1"`, each flagged with `// TODO` comments as not production-ready. confidence 0.9.

## Recommended Next Steps (on DB connect)
1. Row counts on Orders/Baskets to assess real production volume vs. demo data.
2. `pg_constraint` / `information_schema.referential_constraints` (Postgres, not `sp_fkeys`/SQL Server as previously stated) to confirm ON DELETE behavior for CatalogItems → BasketItems/OrderItems FKs.
3. Confirm whether `appsettings.Docker.json`'s SQL Server connection strings are dead config that should be removed, or whether a Docker/SQL Server deployment path still exists in parallel.
