# Business Capability Map

This file groups evidence-derived module candidates into higher-level forward-engineering capability candidates. These are not final bounded contexts until reviewed by architects and product/domain owners.

## Summary

- Capability candidates: 13
- Module candidates grouped: 13
- Components considered: 310
- Interfaces considered: 55

## Capability Candidates

| Capability | Class | Modules | Components | Interfaces | Data Components | Risks | Coupling | Forward Decision | Confidence | Evidence |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| CAP-001 Catalog | DataInfrastructure | 1 | 25 | 9 | 7 | 3 | 13 | review_before_extraction | 0.874 | src/ApplicationCore/CatalogSettings.cs, src/ApplicationCore/Entities/CatalogBrand.cs, src/ApplicationCore/Entities/CatalogItem.cs, and 17 more |
| CAP-002 Identity | DataInfrastructure | 1 | 25 | 29 | 3 | 1 | 8 | review_before_extraction | 0.873 | src/ApplicationCore/Constants/AuthorizationConstants.cs, src/ApplicationCore/Interfaces/ITokenClaimsService.cs, src/BlazorAdmin/CustomAuthStateProvider.cs, and 17 more |
| CAP-003 Verification | TestVerification | 1 | 25 | 0 | 0 | 0 | 0 | review | 0.9 | tests/FunctionalTests/PublicApi/ApiTestFixture.cs, tests/FunctionalTests/PublicApi/ApiTokenHelper.cs, tests/FunctionalTests/Web/Controllers/AccountControllerSignIn.cs, and 17 more |
| CAP-004 Admin | InterfaceCapabilityCandidate | 1 | 23 | 2 | 0 | 1 | 3 | review_before_extraction | 0.776 | src/BlazorAdmin/App.razor, src/BlazorAdmin/Helpers/BlazorComponent.cs, src/BlazorAdmin/Helpers/BlazorLayoutComponent.cs, and 17 more |
| CAP-005 Basket | DataInfrastructure | 1 | 23 | 3 | 3 | 1 | 9 | review_before_extraction | 0.786 | src/ApplicationCore/Entities/BasketAggregate/Basket.cs, src/ApplicationCore/Entities/BasketAggregate/BasketItem.cs, src/ApplicationCore/Exceptions/BasketNotFoundException.cs, and 17 more |
| CAP-006 Controllers | InterfaceCapabilityCandidate | 1 | 21 | 3 | 0 | 1 | 7 | review_before_extraction | 0.711 | src/Web/Controllers/Api/BaseApiController.cs, src/Web/Extensions/CacheHelpers.cs, src/Web/Extensions/EmailSenderExtensions.cs, and 17 more |
| CAP-007 Order | DataInfrastructure | 1 | 21 | 2 | 5 | 1 | 4 | review_before_extraction | 0.894 | src/ApplicationCore/Entities/BuyerAggregate/Buyer.cs, src/ApplicationCore/Entities/BuyerAggregate/PaymentMethod.cs, src/ApplicationCore/Entities/OrderAggregate/Address.cs, and 17 more |
| CAP-008 Application | TechnicalSupport | 1 | 13 | 0 | 2 | 1 | 6 | review | 0.68 | src/ApplicationCore/Entities/BaseEntity.cs, src/ApplicationCore/Exceptions/DuplicateException.cs, src/ApplicationCore/Extensions/JsonExtensions.cs, and 10 more |
| CAP-009 Contracts | UICapabilityCandidate | 1 | 12 | 0 | 0 | 0 | 1 | review | 0.88 | src/BlazorShared/Attributes/EndpointAttribute.cs, src/BlazorShared/BaseUrlConfiguration.cs, src/BlazorShared/Interfaces/ICatalogItemService.cs, and 9 more |
| CAP-010 Cross | InterfaceCapabilityCandidate | 1 | 10 | 7 | 0 | 0 | 4 | review | 0.725 | src/PublicApi/CustomSchemaFilters.cs, src/PublicApi/Middleware/ExceptionMiddleware.cs, src/PublicApi/Program.cs, and 7 more |
| CAP-011 Message | ApplicationCapabilityCandidate | 1 | 5 | 0 | 0 | 0 | 2 | review | 0.68 | src/PublicApi/BaseMessage.cs, src/PublicApi/BaseRequest.cs, src/PublicApi/BaseResponse.cs, and 2 more |
| CAP-012 Infrastructure | ApplicationCapabilityCandidate | 1 | 3 | 0 | 0 | 0 | 4 | review | 0.78 | src/Infrastructure/Dependencies.cs, src/Infrastructure/Logging/LoggerAdapter.cs, src/Infrastructure/Services/EmailSender.cs |
| CAP-013 Data | DataInfrastructure | 1 | 2 | 0 | 2 | 3 | 5 | review_before_extraction | 0.84 | src/Infrastructure/Data/EfRepository.cs, src/Infrastructure/Data/FileItem.cs |

## Review Notes

- Use this map to discuss future module/service boundaries.
- Prefer capabilities with low coupling, clear interfaces, and few risks as earlier modernization candidates.
- Do not split capabilities with shared data ownership or weak evidence until open questions are resolved.
