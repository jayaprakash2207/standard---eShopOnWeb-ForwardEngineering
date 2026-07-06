# Module Consolidation Map

This file consolidates fine-grained static module candidates into higher-level module candidates for enterprise architecture review.

## Summary

- Consolidated candidates: 13
- Consolidate now candidates: 5
- Review before consolidation: 8
- Keep as component/submodule candidates: 0

## Consolidation Candidates

| Consolidated Module | Action | Class | Source Modules | Components | Interfaces | Data | Risks | Coupling | Confidence | Evidence |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| CMOD-001 Catalog | review_before_consolidating | DataInfrastructure | 1 | 25 | 9 | 7 | 3 | 13 | 0.874 | src/ApplicationCore/CatalogSettings.cs, src/ApplicationCore/Entities/CatalogBrand.cs, src/ApplicationCore/Entities/CatalogItem.cs, and 17 more |
| CMOD-002 Identity | review_before_consolidating | DataInfrastructure | 1 | 25 | 29 | 3 | 1 | 8 | 0.873 | src/ApplicationCore/Constants/AuthorizationConstants.cs, src/ApplicationCore/Interfaces/ITokenClaimsService.cs, src/BlazorAdmin/CustomAuthStateProvider.cs, and 17 more |
| CMOD-003 Verification | consolidate_as_candidate_module | TestVerification | 1 | 25 | 0 | 0 | 0 | 0 | 0.9 | tests/FunctionalTests/PublicApi/ApiTestFixture.cs, tests/FunctionalTests/PublicApi/ApiTokenHelper.cs, tests/FunctionalTests/Web/Controllers/AccountControllerSignIn.cs, and 17 more |
| CMOD-004 Admin | review_before_consolidating | InterfaceCapabilityCandidate | 1 | 23 | 2 | 0 | 1 | 3 | 0.776 | src/BlazorAdmin/App.razor, src/BlazorAdmin/Helpers/BlazorComponent.cs, src/BlazorAdmin/Helpers/BlazorLayoutComponent.cs, and 17 more |
| CMOD-005 Basket | review_before_consolidating | DataInfrastructure | 1 | 23 | 3 | 3 | 1 | 9 | 0.786 | src/ApplicationCore/Entities/BasketAggregate/Basket.cs, src/ApplicationCore/Entities/BasketAggregate/BasketItem.cs, src/ApplicationCore/Exceptions/BasketNotFoundException.cs, and 17 more |
| CMOD-006 Controllers | review_before_consolidating | InterfaceCapabilityCandidate | 1 | 21 | 3 | 0 | 1 | 7 | 0.711 | src/Web/Controllers/Api/BaseApiController.cs, src/Web/Extensions/CacheHelpers.cs, src/Web/Extensions/EmailSenderExtensions.cs, and 17 more |
| CMOD-007 Order | review_before_consolidating | DataInfrastructure | 1 | 21 | 2 | 5 | 1 | 4 | 0.894 | src/ApplicationCore/Entities/BuyerAggregate/Buyer.cs, src/ApplicationCore/Entities/BuyerAggregate/PaymentMethod.cs, src/ApplicationCore/Entities/OrderAggregate/Address.cs, and 17 more |
| CMOD-008 Application | review_before_consolidating | TechnicalSupport | 1 | 13 | 0 | 2 | 1 | 6 | 0.68 | src/ApplicationCore/Entities/BaseEntity.cs, src/ApplicationCore/Exceptions/DuplicateException.cs, src/ApplicationCore/Extensions/JsonExtensions.cs, and 10 more |
| CMOD-009 Contracts | consolidate_as_candidate_module | UICapabilityCandidate | 1 | 12 | 0 | 0 | 0 | 1 | 0.88 | src/BlazorShared/Attributes/EndpointAttribute.cs, src/BlazorShared/BaseUrlConfiguration.cs, src/BlazorShared/Interfaces/ICatalogItemService.cs, and 9 more |
| CMOD-010 Cross | consolidate_as_candidate_module | InterfaceCapabilityCandidate | 1 | 10 | 7 | 0 | 0 | 4 | 0.725 | src/PublicApi/CustomSchemaFilters.cs, src/PublicApi/Middleware/ExceptionMiddleware.cs, src/PublicApi/Program.cs, and 7 more |
| CMOD-011 Message | consolidate_as_candidate_module | ApplicationCapabilityCandidate | 1 | 5 | 0 | 0 | 0 | 2 | 0.68 | src/PublicApi/BaseMessage.cs, src/PublicApi/BaseRequest.cs, src/PublicApi/BaseResponse.cs, and 2 more |
| CMOD-012 Infrastructure | consolidate_as_candidate_module | ApplicationCapabilityCandidate | 1 | 3 | 0 | 0 | 0 | 4 | 0.78 | src/Infrastructure/Dependencies.cs, src/Infrastructure/Logging/LoggerAdapter.cs, src/Infrastructure/Services/EmailSender.cs |
| CMOD-013 Data | review_before_consolidating | DataInfrastructure | 1 | 2 | 0 | 2 | 3 | 5 | 0.84 | src/Infrastructure/Data/EfRepository.cs, src/Infrastructure/Data/FileItem.cs |

## How To Use

- Use `consolidate_as_candidate_module` items as starting points for future modular boundaries.
- Use `review_before_consolidating` items for architecture workshops because they have coupling, risk, weak boundary, or data ownership concerns.
- Use `keep_as_component_or_submodule_candidate` items as internal implementation details unless business ownership says otherwise.
