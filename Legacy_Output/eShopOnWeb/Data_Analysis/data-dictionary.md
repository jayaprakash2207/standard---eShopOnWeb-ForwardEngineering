# Data Dictionary — eShopOnWeb

`db_connection: CODE-ONLY — definitions below derived from EF entity structure and naming conventions; values not confirmed against live data.`

## CatalogDb

### CatalogBrands
| Column | Type | Description | Confidence |
|---|---|---|---|
| Id | int | Primary key | 0.8 |
| Brand | string | Display name of the product brand (e.g. "Adventure Works") | 0.8 |

### CatalogTypes
| Column | Type | Description | Confidence |
|---|---|---|---|
| Id | int | Primary key | 0.8 |
| Type | string | Product category name (e.g. "Mugs", "T-Shirts") | 0.8 |

### Catalog (CatalogItem)
| Column | Type | Description | Confidence |
|---|---|---|---|
| Id | int | Primary key | 0.8 |
| Name | string | Product display name | 0.8 |
| Description | string | Long-form product description shown on detail page | 0.75 |
| Price | decimal | Unit sale price | 0.8 |
| PictureUri | string | Path/URL to product image, composed via IUriComposer | 0.75 |
| CatalogTypeId | int (FK) | Category classification → CatalogTypes.Id | 0.8 |
| CatalogBrandId | int (FK) | Brand classification → CatalogBrands.Id | 0.8 |
| AvailableStock | int | Current units available for sale | 0.75 |
| RestockThreshold | int | Stock level below which reorder is triggered | 0.75 |
| MaxStockThreshold | int | Maximum stock level the warehouse will hold | 0.75 |
| OnReorder | bool | Flag indicating a reorder is currently in progress | 0.75 |

### Baskets (Basket)
| Column | Type | Description | Confidence |
|---|---|---|---|
| Id | int | Primary key | 0.8 |
| BuyerId | string | Soft reference to AspNetUsers.Id (IdentityDb) — identifies the basket's owner | 0.8 |

### BasketItems (BasketItem)
| Column | Type | Description | Confidence |
|---|---|---|---|
| Id | int | Primary key | 0.8 |
| BasketId | int (FK) | → Baskets.Id | 0.8 |
| CatalogItemId | int (FK) | → Catalog.Id | 0.8 |
| UnitPrice | decimal | Price captured at time of adding to basket | 0.75 |
| Quantity | int | Number of units of this item in the basket | 0.75 |

### Orders (Order)
| Column | Type | Description | Confidence |
|---|---|---|---|
| Id | int | Primary key | 0.8 |
| BuyerId | string | Soft reference to AspNetUsers.Id (IdentityDb) — who placed the order | 0.8 |
| OrderDate | datetime | Date/time the order was placed | 0.8 |
| ShipToAddress_Street | string | Shipping address — street (owned type Address, flattened) | 0.75 |
| ShipToAddress_City | string | Shipping address — city | 0.75 |
| ShipToAddress_State | string | Shipping address — state/province | 0.75 |
| ShipToAddress_Country | string | Shipping address — country | 0.75 |
| ShipToAddress_ZipCode | string | Shipping address — postal code | 0.75 |

### OrderItems (OrderItem)
| Column | Type | Description | Confidence |
|---|---|---|---|
| Id | int | Primary key | 0.8 |
| OrderId | int (FK) | → Orders.Id | 0.8 |
| ItemOrdered_CatalogItemId | int | Snapshot of the catalog item id at time of order (not a live FK) | 0.75 |
| ItemOrdered_ProductName | string | Snapshot of product name at time of order | 0.75 |
| ItemOrdered_PictureUri | string | Snapshot of product image path at time of order | 0.75 |
| UnitPrice | decimal | Price paid per unit | 0.75 |
| Units | int | Quantity ordered | 0.75 |

## IdentityDb (INFERRED — standard ASP.NET Core Identity, confidence 0.7)

### AspNetUsers
| Column | Type | Description | Confidence |
|---|---|---|---|
| Id | string (GUID) | Primary key, referenced by Baskets.BuyerId / Orders.BuyerId | 0.7 |
| UserName | string | Login username, typically equal to Email | 0.7 |
| Email | string | User's email address | 0.7 |
| PasswordHash | string | Hashed password (ASP.NET Identity) | 0.7 |
| PhoneNumber | string | Optional phone number | 0.65 |

### AspNetRoles
| Column | Type | Description | Confidence |
|---|---|---|---|
| Id | string (GUID) | Primary key | 0.7 |
| Name | string | Role name, e.g. "Administrators" (see AuthorizationConstants / Roles classes) | 0.75 |

### AspNetUserRoles
| Column | Type | Description | Confidence |
|---|---|---|---|
| UserId | string (FK) | → AspNetUsers.Id | 0.7 |
| RoleId | string (FK) | → AspNetRoles.Id | 0.7 |

## Unmapped / Unconfirmed Entities
| Entity | Notes | Confidence |
|---|---|---|
| Buyer | CONFIRMED dead/unmapped code (RC-002) — not a DbSet on CatalogContext, no EF configuration found. See redundancy-analysis.json | 0.9 |
| PaymentMethod | CONFIRMED dead/unmapped code (RC-002) — not persisted, not currently PCI-DSS scope. See pii-inventory.json | 0.9 |
| CatalogItemDetails | struct, likely a non-persisted DTO/projection | 0.7 |

## Change Records
- **RC-002** (CORRECTED): Buyer and PaymentMethod confirmed dead/unmapped code, confidence 0.6 → 0.9.
