=== DOCUMENT: 07_DATA_MODEL_SPECIFICATION.md ===

# Data Model Specification — eShopOnWeb
## Physical Schema, EF Configuration, and SQL DDL

---

## 1. Database Overview

| Database | Engine | Version | Access Pattern | Migration Tool |
|----------|--------|---------|----------------|----------------|
| CatalogDB | SQL Server / Azure SQL | v12.0 | EF Core 8 (code-first) | dotnet-ef migrations |
| IdentityDB | SQL Server / Azure SQL | v12.0 | EF Core 8 (IdentityDbContext) | dotnet-ef migrations |

Both databases share the same SQL Server instance in Docker dev. In Azure production, each has its own Azure SQL Server resource.

---

## 2. EF Core Context Configuration

### CatalogContext

```csharp
// src/Infrastructure/Data/CatalogContext.cs
public class CatalogContext : DbContext
{
    public DbSet<CatalogItem> CatalogItems { get; set; }
    public DbSet<CatalogBrand> CatalogBrands { get; set; }
    public DbSet<CatalogType> CatalogTypes { get; set; }
    // Basket, Order, OrderItem, BasketItem registered via ApplyConfigurationsFromAssembly

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        builder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }
}
```

### Key EF Fluent Configurations

**CatalogItem (catalog_hilo HiLo sequence):**
```csharp
builder.Property(ci => ci.Id).UseHiLo("catalog_hilo");
builder.Property(ci => ci.Name).IsRequired();
builder.HasOne(ci => ci.CatalogBrand).WithMany().HasForeignKey(ci => ci.CatalogBrandId);
builder.HasOne(ci => ci.CatalogType).WithMany().HasForeignKey(ci => ci.CatalogTypeId);
```

**Order (owned Address value object):**
```csharp
builder.OwnsOne(o => o.ShipToAddress, a => {
    a.WithOwner();
    a.Property(x => x.ZipCode).HasMaxLength(18).IsRequired();
    a.Property(x => x.Street).HasMaxLength(180).IsRequired();
    a.Property(x => x.State).HasMaxLength(60).IsRequired();
    a.Property(x => x.Country).HasMaxLength(90).IsRequired();
    a.Property(x => x.City).HasMaxLength(100).IsRequired();
});
builder.Navigation(x => x.ShipToAddress).IsRequired();
```

**OrderItem (owned CatalogItemOrdered value object):**
```csharp
builder.OwnsOne(i => i.ItemOrdered);
```

---

## 3. SQL DDL — CatalogDB

```sql
-- Sequence for CatalogItem HiLo key generation
CREATE SEQUENCE [catalog_hilo]
    START WITH 1
    INCREMENT BY 10;

-- CatalogBrands
CREATE TABLE [CatalogBrands] (
    [Id]    INT IDENTITY(1,1) NOT NULL,
    [Brand] NVARCHAR(MAX)     NOT NULL,
    CONSTRAINT [PK_CatalogBrands] PRIMARY KEY ([Id])
);

-- CatalogTypes
CREATE TABLE [CatalogTypes] (
    [Id]   INT IDENTITY(1,1) NOT NULL,
    [Type] NVARCHAR(MAX)     NOT NULL,
    CONSTRAINT [PK_CatalogTypes] PRIMARY KEY ([Id])
);

-- CatalogItems
CREATE TABLE [CatalogItems] (
    [Id]             INT           NOT NULL DEFAULT (NEXT VALUE FOR [catalog_hilo]),
    [Name]           NVARCHAR(MAX) NOT NULL,
    [Description]    NVARCHAR(MAX) NOT NULL,
    [Price]          DECIMAL(18,2) NOT NULL,
    [PictureUri]     NVARCHAR(MAX) NOT NULL,
    [CatalogTypeId]  INT           NOT NULL,
    [CatalogBrandId] INT           NOT NULL,
    CONSTRAINT [PK_CatalogItems]         PRIMARY KEY ([Id]),
    CONSTRAINT [FK_CatalogItems_Types]   FOREIGN KEY ([CatalogTypeId])  REFERENCES [CatalogTypes]([Id]),
    CONSTRAINT [FK_CatalogItems_Brands]  FOREIGN KEY ([CatalogBrandId]) REFERENCES [CatalogBrands]([Id])
);
-- RECOMMENDED: Add unique index on Name (DQ-001 gap)
-- CREATE UNIQUE INDEX [UX_CatalogItems_Name] ON [CatalogItems] ([Name]);

-- Baskets
CREATE TABLE [Baskets] (
    [Id]      INT IDENTITY(1,1) NOT NULL,
    [BuyerId] NVARCHAR(MAX)     NOT NULL,  -- PII: email or anonymous GUID
    CONSTRAINT [PK_Baskets] PRIMARY KEY ([Id])
);

-- BasketItems
CREATE TABLE [BasketItems] (
    [Id]            INT           IDENTITY(1,1) NOT NULL,
    [UnitPrice]     DECIMAL(18,2) NOT NULL,
    [Quantity]      INT           NOT NULL,
    [CatalogItemId] INT           NOT NULL,  -- Soft ref; no FK constraint
    [BasketId]      INT           NOT NULL,
    CONSTRAINT [PK_BasketItems]          PRIMARY KEY ([Id]),
    CONSTRAINT [FK_BasketItems_Baskets]  FOREIGN KEY ([BasketId]) REFERENCES [Baskets]([Id]) ON DELETE CASCADE
);

-- Orders
CREATE TABLE [Orders] (
    [Id]                       INT                  IDENTITY(1,1) NOT NULL,
    [BuyerId]                  NVARCHAR(MAX)         NOT NULL,  -- PII: email
    [OrderDate]                DATETIMEOFFSET(7)     NOT NULL,
    [ShipToAddress_Street]     NVARCHAR(180)         NOT NULL,  -- PII
    [ShipToAddress_City]       NVARCHAR(100)         NOT NULL,  -- PII
    [ShipToAddress_State]      NVARCHAR(60)          NOT NULL,  -- PII
    [ShipToAddress_Country]    NVARCHAR(90)          NOT NULL,  -- PII
    [ShipToAddress_ZipCode]    NVARCHAR(18)          NOT NULL,  -- PII
    CONSTRAINT [PK_Orders] PRIMARY KEY ([Id])
);

-- OrderItems
CREATE TABLE [OrderItems] (
    [Id]                         INT           IDENTITY(1,1) NOT NULL,
    [OrderId]                    INT           NOT NULL,
    [ItemOrdered_CatalogItemId]  INT           NOT NULL,
    [ItemOrdered_ProductName]    NVARCHAR(MAX) NOT NULL,  -- Snapshot (immutable)
    [ItemOrdered_PictureUri]     NVARCHAR(MAX) NOT NULL,  -- Snapshot (immutable)
    [UnitPrice]                  DECIMAL(18,2) NOT NULL,
    [Units]                      INT           NOT NULL,
    CONSTRAINT [PK_OrderItems]        PRIMARY KEY ([Id]),
    CONSTRAINT [FK_OrderItems_Orders] FOREIGN KEY ([OrderId]) REFERENCES [Orders]([Id]) ON DELETE CASCADE
);
```

---

## 4. SQL DDL — IdentityDB (ASP.NET Core Identity Standard Schema)

```sql
CREATE TABLE [AspNetUsers] (
    [Id]                   NVARCHAR(450)    NOT NULL,
    [UserName]             NVARCHAR(256)    NULL,
    [NormalizedUserName]   NVARCHAR(256)    NULL,
    [Email]                NVARCHAR(256)    NULL,  -- PII
    [NormalizedEmail]      NVARCHAR(256)    NULL,
    [EmailConfirmed]       BIT              NOT NULL DEFAULT 0,
    [PasswordHash]         NVARCHAR(MAX)    NULL,  -- Sensitive: PBKDF2
    [SecurityStamp]        NVARCHAR(MAX)    NULL,
    [ConcurrencyStamp]     NVARCHAR(MAX)    NULL,
    [PhoneNumber]          NVARCHAR(MAX)    NULL,
    [PhoneNumberConfirmed] BIT              NOT NULL DEFAULT 0,
    [TwoFactorEnabled]     BIT              NOT NULL DEFAULT 0,
    [LockoutEnd]           DATETIMEOFFSET(7) NULL,
    [LockoutEnabled]       BIT              NOT NULL DEFAULT 0,
    [AccessFailedCount]    INT              NOT NULL DEFAULT 0,
    CONSTRAINT [PK_AspNetUsers] PRIMARY KEY ([Id])
);
CREATE UNIQUE INDEX [UserNameIndex]  ON [AspNetUsers] ([NormalizedUserName]) WHERE [NormalizedUserName] IS NOT NULL;
CREATE INDEX        [EmailIndex]     ON [AspNetUsers] ([NormalizedEmail]) WHERE [NormalizedEmail] IS NOT NULL;

CREATE TABLE [AspNetRoles] (
    [Id]               NVARCHAR(450) NOT NULL,
    [Name]             NVARCHAR(256) NULL,
    [NormalizedName]   NVARCHAR(256) NULL,
    [ConcurrencyStamp] NVARCHAR(MAX) NULL,
    CONSTRAINT [PK_AspNetRoles] PRIMARY KEY ([Id])
);
CREATE UNIQUE INDEX [RoleNameIndex] ON [AspNetRoles] ([NormalizedName]) WHERE [NormalizedName] IS NOT NULL;

CREATE TABLE [AspNetUserRoles] (
    [UserId] NVARCHAR(450) NOT NULL,
    [RoleId] NVARCHAR(450) NOT NULL,
    CONSTRAINT [PK_AspNetUserRoles] PRIMARY KEY ([UserId],[RoleId]),
    CONSTRAINT [FK_AspNetUserRoles_Users] FOREIGN KEY ([UserId]) REFERENCES [AspNetUsers]([Id]) ON DELETE CASCADE,
    CONSTRAINT [FK_AspNetUserRoles_Roles] FOREIGN KEY ([RoleId]) REFERENCES [AspNetRoles]([Id]) ON DELETE CASCADE
);

-- AspNetUserClaims, AspNetUserLogins, AspNetUserTokens, AspNetRoleClaims follow standard Identity schema (omitted for brevity)
```

---

## 5. EF Migrations Summary

### CatalogDB Migrations

| Migration | Timestamp | Description |
|-----------|-----------|-------------|
| 20201202175935_InitialModel | 2020-12-02 | Creates all 7 CatalogDB tables + catalog_hilo sequence |
| 20211022172603_FixBuyerId | 2021-10-22 | Adjusts BuyerId column on Baskets or Orders |
| 20211129215029_FixShipToAddress | 2021-11-29 | Updates ShipToAddress owned entity column constraints |

### IdentityDB Migrations

| Migration | Timestamp | Description |
|-----------|-----------|-------------|
| 20201202175808_InitialIdentityModel | 2020-12-02 | Creates all 7 standard ASP.NET Identity tables |

---

## 6. Data Quality Gaps (Forward Engineering Recommendations)

| Gap | Risk | Recommended Fix |
|-----|------|----------------|
| No UNIQUE index on CatalogItems.Name | Duplicate names allowed at DB level; only API-enforced | Add: `CREATE UNIQUE INDEX [UX_CatalogItems_Name] ON [CatalogItems] ([Name]);` |
| No FK on BasketItems.CatalogItemId | Orphaned basket items possible after product deletion | Add FK or accept soft-reference; requires business decision |
| No OrderStatus column on Orders | No lifecycle tracking | Add: `OrderStatus NVARCHAR(50) NOT NULL DEFAULT 'Pending'` with check constraint |
| BuyerId stored as NVARCHAR(MAX) | No length constraint; inefficient indexing | Change to NVARCHAR(256) with index |
| No expiry column on Baskets | Anonymous baskets never expire | Add: `CreatedAt DATETIMEOFFSET NOT NULL DEFAULT SYSUTCDATETIME()` + cleanup job |
| EF InMemory in tests bypasses all constraints | FK/UNIQUE/NULL violations untested | Run at least one integration test suite against real SQL Server |
