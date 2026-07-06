# Data Ownership Map

This is application-architecture ownership evidence, not a database design document.

## Entity Ownership Candidates

| Entity | Component ID | Module | Capability | File | Confidence |
|---|---|---|---|---|---:|
| BaseEntity | COMP-0003 | ApplicationCore | CAP-008 Application | src/ApplicationCore/Entities/BaseEntity.cs | 0.96 |
| CatalogBrand | COMP-0004 | Catalog | CAP-001 Catalog | src/ApplicationCore/Entities/CatalogBrand.cs | 0.96 |
| CatalogItem | COMP-0005 | Catalog | CAP-001 Catalog | src/ApplicationCore/Entities/CatalogItem.cs | 0.96 |
| CatalogItemDetails | COMP-0006 | Catalog | CAP-001 Catalog | src/ApplicationCore/Entities/CatalogItem.cs | 0.96 |
| CatalogType | COMP-0007 | Catalog | CAP-001 Catalog | src/ApplicationCore/Entities/CatalogType.cs | 0.96 |
| Basket | COMP-0008 | Basket | CAP-005 Basket | src/ApplicationCore/Entities/BasketAggregate/Basket.cs | 0.96 |
| BasketItem | COMP-0009 | Basket | CAP-005 Basket | src/ApplicationCore/Entities/BasketAggregate/BasketItem.cs | 0.96 |
| Buyer | COMP-0010 | Order | CAP-007 Order | src/ApplicationCore/Entities/BuyerAggregate/Buyer.cs | 0.96 |
| PaymentMethod | COMP-0011 | Order | CAP-007 Order | src/ApplicationCore/Entities/BuyerAggregate/PaymentMethod.cs | 0.96 |
| Address | COMP-0012 | Order | CAP-007 Order | src/ApplicationCore/Entities/OrderAggregate/Address.cs | 0.96 |
| CatalogItemOrdered | COMP-0013 | Catalog | CAP-001 Catalog | src/ApplicationCore/Entities/OrderAggregate/CatalogItemOrdered.cs | 0.96 |
| Order | COMP-0014 | Order | CAP-007 Order | src/ApplicationCore/Entities/OrderAggregate/Order.cs | 0.96 |
| OrderItem | COMP-0015 | Order | CAP-007 Order | src/ApplicationCore/Entities/OrderAggregate/OrderItem.cs | 0.96 |
| IAggregateRoot | COMP-0021 | ApplicationCore | CAP-008 Application | src/ApplicationCore/Interfaces/IAggregateRoot.cs | 0.96 |
| ApplicationUser | COMP-0099 | Identity | CAP-002 Identity | src/Infrastructure/Identity/ApplicationUser.cs | 0.96 |
| BasketAddItem | COMP-0226 | Verification | CAP-003 Verification | tests/UnitTests/ApplicationCore/Entities/BasketTests/BasketAddItem.cs | 0.96 |
| BasketRemoveEmptyItems | COMP-0227 | Verification | CAP-003 Verification | tests/UnitTests/ApplicationCore/Entities/BasketTests/BasketRemoveEmptyItems.cs | 0.96 |
| BasketTotalItems | COMP-0228 | Verification | CAP-003 Verification | tests/UnitTests/ApplicationCore/Entities/BasketTests/BasketTotalItems.cs | 0.96 |
| OrderTotal | COMP-0229 | Verification | CAP-003 Verification | tests/UnitTests/ApplicationCore/Entities/OrderTests/OrderTotal.cs | 0.96 |

## Repository / Data Access Candidates

| Component | Component ID | Type | Layer | Module | Capability | File | Risk Note |
|---|---|---|---|---|---|---|---|
| IReadRepository | COMP-0027 | Repository | DataAccess | ApplicationCore | CAP-008 Application | src/ApplicationCore/Interfaces/IReadRepository.cs | review shared ownership |
| IRepository | COMP-0028 | Repository | DataAccess | ApplicationCore | CAP-008 Application | src/ApplicationCore/Interfaces/IRepository.cs | review shared ownership |
| BasketWithItemsSpecification | COMP-0034 | Repository | DataAccess | Basket | CAP-005 Basket | src/ApplicationCore/Specifications/BasketWithItemsSpecification.cs | review shared ownership |
| CatalogFilterPaginatedSpecification | COMP-0035 | Repository | DataAccess | Catalog | CAP-001 Catalog | src/ApplicationCore/Specifications/CatalogFilterPaginatedSpecification.cs | review shared ownership |
| CatalogFilterSpecification | COMP-0036 | Repository | DataAccess | Catalog | CAP-001 Catalog | src/ApplicationCore/Specifications/CatalogFilterSpecification.cs | review shared ownership |
| CatalogItemNameSpecification | COMP-0037 | Repository | DataAccess | Catalog | CAP-001 Catalog | src/ApplicationCore/Specifications/CatalogItemNameSpecification.cs | review shared ownership |
| CatalogItemsSpecification | COMP-0038 | Repository | DataAccess | Catalog | CAP-001 Catalog | src/ApplicationCore/Specifications/CatalogItemsSpecification.cs | review shared ownership |
| CustomerOrdersSpecification | COMP-0039 | Repository | DataAccess | Order | CAP-007 Order | src/ApplicationCore/Specifications/CustomerOrdersSpecification.cs | review shared ownership |
| CustomerOrdersWithItemsSpecification | COMP-0040 | Repository | DataAccess | Order | CAP-007 Order | src/ApplicationCore/Specifications/CustomerOrdersWithItemsSpecification.cs | review shared ownership |
| OrderWithItemsByIdSpec | COMP-0041 | Repository | DataAccess | Order | CAP-007 Order | src/ApplicationCore/Specifications/OrderWithItemsByIdSpec.cs | review shared ownership |
| CatalogContext | COMP-0085 | Repository | DataAccess | Catalog | CAP-001 Catalog | src/Infrastructure/Data/CatalogContext.cs | review shared ownership |
| EfRepository | COMP-0087 | Repository | DataAccess | DataAccess | CAP-013 Data | src/Infrastructure/Data/EfRepository.cs | review shared ownership |
| AppIdentityDbContext | COMP-0097 | Repository | DataAccess | Identity | CAP-002 Identity | src/Infrastructure/Identity/AppIdentityDbContext.cs | review shared ownership |
| CatalogContextSeed | COMP-0086 | BatchJob | DataAccess | Catalog | CAP-001 Catalog | src/Infrastructure/Data/CatalogContextSeed.cs | review shared ownership |
| FileItem | COMP-0088 | DTO | Infrastructure | DataAccess | CAP-013 Data | src/Infrastructure/Data/FileItem.cs | review |
| BasketConfiguration | COMP-0089 | Configuration | Infrastructure | Basket | CAP-005 Basket | src/Infrastructure/Data/Config/BasketConfiguration.cs | review |
| BasketItemConfiguration | COMP-0090 | Configuration | Infrastructure | Basket | CAP-005 Basket | src/Infrastructure/Data/Config/BasketItemConfiguration.cs | review |
| CatalogBrandConfiguration | COMP-0091 | Configuration | Infrastructure | Catalog | CAP-001 Catalog | src/Infrastructure/Data/Config/CatalogBrandConfiguration.cs | review |
| CatalogItemConfiguration | COMP-0092 | Configuration | Infrastructure | Catalog | CAP-001 Catalog | src/Infrastructure/Data/Config/CatalogItemConfiguration.cs | review |
| CatalogTypeConfiguration | COMP-0093 | Configuration | Infrastructure | Catalog | CAP-001 Catalog | src/Infrastructure/Data/Config/CatalogTypeConfiguration.cs | review |
| OrderConfiguration | COMP-0094 | Configuration | Infrastructure | Order | CAP-007 Order | src/Infrastructure/Data/Config/OrderConfiguration.cs | review |
| OrderItemConfiguration | COMP-0095 | Configuration | Infrastructure | Order | CAP-007 Order | src/Infrastructure/Data/Config/OrderItemConfiguration.cs | review |
| AppIdentityDbContextSeed | COMP-0098 | BatchJob | DataAccess | Identity | CAP-002 Identity | src/Infrastructure/Identity/AppIdentityDbContextSeed.cs | review shared ownership |
| ApplicationUser | COMP-0099 | Entity | Infrastructure | Identity | CAP-002 Identity | src/Infrastructure/Identity/ApplicationUser.cs | review |

## Forward Engineering Guidance

- Do not extract a capability as a separate service until entity and repository ownership are confirmed.
- Shared repositories or data-access abstractions should be wrapped, split, or explicitly owned before service extraction.
- Use this map with `dependency-graph.json` and `application-risk-register.json` before choosing persistence boundaries.
