# Architecture Decision Inputs

These are decision prompts for architects. They are derived from extracted evidence and should be resolved before committing to future boundaries.

## ADR-INPUT-001: Confirm `Catalog` Boundary

Decision needed: Should `Catalog` be a separate future module/service boundary, remain internal, or merge with another capability?

Evidence: CAP-001; modules MOD-004 Catalog; source files src/ApplicationCore/CatalogSettings.cs, src/ApplicationCore/Entities/CatalogBrand.cs, src/ApplicationCore/Entities/CatalogItem.cs, src/ApplicationCore/Entities/CatalogType.cs, and 16 more.

Risk signal: risks 3, weak modules 1, coupling 13.

Recommended review: confirm ownership, public interfaces, data ownership, and call flows before extraction.

## ADR-INPUT-002: Confirm `Identity` Boundary

Decision needed: Should `Identity` be a separate future module/service boundary, remain internal, or merge with another capability?

Evidence: CAP-002; modules MOD-007 Identity; source files src/ApplicationCore/Constants/AuthorizationConstants.cs, src/ApplicationCore/Interfaces/ITokenClaimsService.cs, src/BlazorAdmin/CustomAuthStateProvider.cs, src/BlazorAdmin/Pages/Logout.razor, and 16 more.

Risk signal: risks 1, weak modules 1, coupling 8.

Recommended review: confirm ownership, public interfaces, data ownership, and call flows before extraction.

## ADR-INPUT-003: Confirm `Admin` Boundary

Decision needed: Should `Admin` be a separate future module/service boundary, remain internal, or merge with another capability?

Evidence: CAP-004; modules MOD-001 Admin; source files src/BlazorAdmin/App.razor, src/BlazorAdmin/Helpers/BlazorComponent.cs, src/BlazorAdmin/Helpers/BlazorLayoutComponent.cs, src/BlazorAdmin/Helpers/RefreshBroadcast.cs, and 16 more.

Risk signal: risks 1, weak modules 1, coupling 3.

Recommended review: confirm ownership, public interfaces, data ownership, and call flows before extraction.

## ADR-INPUT-004: Confirm `Basket` Boundary

Decision needed: Should `Basket` be a separate future module/service boundary, remain internal, or merge with another capability?

Evidence: CAP-005; modules MOD-003 Basket; source files src/ApplicationCore/Entities/BasketAggregate/Basket.cs, src/ApplicationCore/Entities/BasketAggregate/BasketItem.cs, src/ApplicationCore/Exceptions/BasketNotFoundException.cs, src/ApplicationCore/Exceptions/EmptyBasketOnCheckoutException.cs, and 16 more.

Risk signal: risks 1, weak modules 1, coupling 9.

Recommended review: confirm ownership, public interfaces, data ownership, and call flows before extraction.

## ADR-INPUT-005: Confirm `Controllers` Boundary

Decision needed: Should `Controllers` be a separate future module/service boundary, remain internal, or merge with another capability?

Evidence: CAP-006; modules MOD-013 Web; source files src/Web/Controllers/Api/BaseApiController.cs, src/Web/Extensions/CacheHelpers.cs, src/Web/Extensions/EmailSenderExtensions.cs, src/Web/Extensions/UrlHelperExtensions.cs, and 16 more.

Risk signal: risks 1, weak modules 1, coupling 7.

Recommended review: confirm ownership, public interfaces, data ownership, and call flows before extraction.

## ADR-INPUT-006: Confirm `Order` Boundary

Decision needed: Should `Order` be a separate future module/service boundary, remain internal, or merge with another capability?

Evidence: CAP-007; modules MOD-009 Order; source files src/ApplicationCore/Entities/BuyerAggregate/Buyer.cs, src/ApplicationCore/Entities/BuyerAggregate/PaymentMethod.cs, src/ApplicationCore/Entities/OrderAggregate/Address.cs, src/ApplicationCore/Entities/OrderAggregate/Order.cs, and 16 more.

Risk signal: risks 1, weak modules 1, coupling 4.

Recommended review: confirm ownership, public interfaces, data ownership, and call flows before extraction.

## ADR-INPUT-007: Confirm `Data` Boundary

Decision needed: Should `Data` be a separate future module/service boundary, remain internal, or merge with another capability?

Evidence: CAP-013; modules MOD-006 DataAccess; source files src/Infrastructure/Data/EfRepository.cs, src/Infrastructure/Data/FileItem.cs.

Risk signal: risks 3, weak modules 1, coupling 5.

Recommended review: confirm ownership, public interfaces, data ownership, and call flows before extraction.

## ADR-INPUT-008: Resolve Open Question

Decision needed: Confirm the authoritative system name; evidence packs leave system_name as unknown.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.

## ADR-INPUT-009: Resolve Open Question

Decision needed: Confirm ownership and boundaries for weak or unknown module candidates: Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.

## ADR-INPUT-010: Resolve Open Question

Decision needed: Review the 0 components with unknown module ownership before finalizing module boundaries.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.

## ADR-INPUT-011: Resolve Open Question

Decision needed: Review the 40 components with Unknown type/layer classification to decide whether they are architecture-significant.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.

## ADR-INPUT-012: Resolve Open Question

Decision needed: Review 0 partial call flows before using them as behavior-preservation contracts.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.

## ADR-INPUT-013: Resolve Open Question

Decision needed: Confirm whether detected module cycles are real architecture cycles or artifacts of static dependency resolution: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.

## ADR-INPUT-014: Resolve Open Question

Decision needed: Confirm deployment ownership for detected frontend applications: BlazorAdmin.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.

## ADR-INPUT-015: Resolve Open Question

Decision needed: Confirm whether detected database/infrastructure services are development-only or production-relevant external boundaries.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.

## ADR-INPUT-016: Resolve Open Question

Decision needed: Confirm the target systems and purposes behind configured HTTP/API base URLs and health-check dependencies: sqlserver, catalog-items, catalog-items/{id}, catalog-items?PageSize=10, {_apiUrl}{uri}.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.

## ADR-INPUT-017: Resolve Open Question

Decision needed: Confirm whether no scheduled jobs/message consumers exist; none were detected in parsed facts.

Evidence: `open-questions.md` and related final JSON artifacts.

Recommended review: assign to architecture/product/application owner and record preserve/redesign/review decision.
