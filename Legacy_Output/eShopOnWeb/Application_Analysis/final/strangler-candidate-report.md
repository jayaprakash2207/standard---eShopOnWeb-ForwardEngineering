# Strangler Candidate Report

Generated from source-backed evidence packs. This report ranks candidates for future extraction or modernization; it does not choose a future technology stack.

## 1. Best Early Extraction/Migration Candidates

No module met the Good Early Candidate rule from current evidence.

## 2. Medium-Risk Candidates

| Module | Score | Coupling | Boundary | External Risk | Reason | Evidence refs |
|---|---:|---:|---|---|---|---|
| PublicApi | 70 | 2 | Medium | review | low coupling but public interface or ownership needs review | MOD-010; COMP-0104; COMP-0105; COMP-0106; COMP-0108; DEP-0149; DEP-0150; DEP-0152; DEP-0154; APP-RISK-003; APP-RISK-004; APP-RISK-005; APP-RISK-006; files: src/PublicApi/BaseMessage.cs, src/PublicApi/BaseRequest.cs, src/PublicApi/BaseResponse.cs |
| SharedContracts | 70 | 1 | Medium | review | low coupling but public interface or ownership needs review | MOD-011; COMP-0063; COMP-0064; COMP-0305; COMP-0081; DEP-0008; DEP-0009; DEP-0010; DEP-0030; APP-RISK-003; APP-RISK-004; APP-RISK-005; APP-RISK-006; files: src/BlazorShared/Attributes/EndpointAttribute.cs, src/BlazorShared/BaseUrlConfiguration.cs, src/BlazorShared/Interfaces/ICatalogItemService.cs |
| Verification | 70 | 0 | Medium | review | low coupling but public interface or ownership needs review | MOD-012; COMP-0209; COMP-0233; COMP-0242; COMP-0206; APP-RISK-003; APP-RISK-004; APP-RISK-005; APP-RISK-006; files: tests/FunctionalTests/PublicApi/ApiTestFixture.cs, tests/FunctionalTests/PublicApi/ApiTokenHelper.cs, tests/FunctionalTests/Web/Controllers/AccountControllerSignIn.cs |
| CrossCutting | 55 | 4 | Medium | review | moderate coupling | MOD-005; COMP-0149; COMP-0150; COMP-0151; COMP-0139; DEP-0018; DEP-0019; DEP-0020; DEP-0146; APP-RISK-003; APP-RISK-004; APP-RISK-005; APP-RISK-006; files: src/PublicApi/CustomSchemaFilters.cs, src/PublicApi/Middleware/ExceptionMiddleware.cs, src/PublicApi/Program.cs |
| Infrastructure | 55 | 4 | Medium | review | moderate coupling | MOD-008; COMP-0084; COMP-0103; COMP-0102; DEP-0018; DEP-0032; DEP-0036; DEP-0047; APP-RISK-003; APP-RISK-004; APP-RISK-005; APP-RISK-006; files: src/Infrastructure/Dependencies.cs, src/Infrastructure/Logging/LoggerAdapter.cs, src/Infrastructure/Services/EmailSender.cs |

## 3. Poor Candidates

| Module | Score | Coupling | Boundary | External Risk | Reason | Evidence refs |
|---|---:|---:|---|---|---|---|
| Admin | 20 | 3 | Weak | review | cycle or high coupling | MOD-001; COMP-0250; COMP-0045; COMP-0046; COMP-0054; DEP-0011; DEP-0029; DEP-0039; DEP-0132; APP-RISK-002; APP-RISK-003; APP-RISK-004; APP-RISK-005; files: src/BlazorAdmin/App.razor, src/BlazorAdmin/Helpers/BlazorComponent.cs, src/BlazorAdmin/Helpers/BlazorLayoutComponent.cs |
| ApplicationCore | 20 | 6 | Weak | review | cycle or high coupling | MOD-002; COMP-0003; COMP-0017; COMP-0021; COMP-0022; DEP-0003; DEP-0004; DEP-0005; DEP-0006; APP-RISK-002; APP-RISK-003; APP-RISK-004; APP-RISK-005; files: src/ApplicationCore/Entities/BaseEntity.cs, src/ApplicationCore/Exceptions/DuplicateException.cs, src/ApplicationCore/Extensions/JsonExtensions.cs |
| Basket | 20 | 9 | Weak | review | cycle or high coupling | MOD-003; COMP-0008; COMP-0179; COMP-0184; COMP-0089; DEP-0003; DEP-0004; DEP-0013; DEP-0023; APP-RISK-002; APP-RISK-003; APP-RISK-004; APP-RISK-005; files: src/ApplicationCore/Entities/BasketAggregate/Basket.cs, src/ApplicationCore/Entities/BasketAggregate/BasketItem.cs, src/ApplicationCore/Exceptions/BasketNotFoundException.cs |
| Catalog | 20 | 13 | Weak | review | cycle or high coupling | MOD-004; COMP-0055; COMP-0056; COMP-0181; COMP-0004; DEP-0001; DEP-0002; DEP-0007; DEP-0008; APP-RISK-001; APP-RISK-002; APP-RISK-003; APP-RISK-004; files: src/ApplicationCore/CatalogSettings.cs, src/ApplicationCore/Entities/CatalogBrand.cs, src/ApplicationCore/Entities/CatalogItem.cs |
| DataAccess | 20 | 5 | Weak | review | cycle or high coupling | MOD-006; COMP-0087; COMP-0088; DEP-0012; DEP-0031; DEP-0033; DEP-0034; APP-RISK-002; APP-RISK-003; APP-RISK-004; APP-RISK-005; files: src/Infrastructure/Data/EfRepository.cs, src/Infrastructure/Data/FileItem.cs |
| Identity | 20 | 8 | Weak | review | cycle or high coupling | MOD-007; COMP-0097; COMP-0098; COMP-0099; COMP-0115; DEP-0014; DEP-0020; DEP-0021; DEP-0022; APP-RISK-002; APP-RISK-003; APP-RISK-004; APP-RISK-005; files: src/ApplicationCore/Constants/AuthorizationConstants.cs, src/ApplicationCore/Interfaces/ITokenClaimsService.cs, src/BlazorAdmin/CustomAuthStateProvider.cs |
| Order | 20 | 4 | Weak | review | cycle or high coupling | MOD-009; COMP-0012; COMP-0010; COMP-0039; COMP-0040; DEP-0001; DEP-0002; DEP-0005; DEP-0006; APP-RISK-002; APP-RISK-003; APP-RISK-004; APP-RISK-005; files: src/ApplicationCore/Entities/BuyerAggregate/Buyer.cs, src/ApplicationCore/Entities/BuyerAggregate/PaymentMethod.cs, src/ApplicationCore/Entities/OrderAggregate/Address.cs |
| Web | 20 | 7 | Weak | review | cycle or high coupling | MOD-013; COMP-0164; COMP-0156; COMP-0157; COMP-0158; DEP-0024; DEP-0025; DEP-0026; DEP-0027; APP-RISK-002; APP-RISK-003; APP-RISK-004; APP-RISK-005; files: src/Web/Controllers/Api/BaseApiController.cs, src/Web/Extensions/CacheHelpers.cs, src/Web/Extensions/EmailSenderExtensions.cs |

## 4. Reasoning

Best early candidates have low efferent coupling and observable interfaces. Current best candidates from evidence are: none detected.

Poor candidates are riskier because dependency evidence reports high coupling, weak/unknown boundaries, and/or module-cycle participation. Current poor candidates from evidence are: Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web.

## 5. Coupling Score

Coupling score here is afferent plus efferent module coupling from `dependency-pack.json`. High values make first extraction riskier.

## 6. Boundary Clarity

Boundary quality is strongest where source folders, entry points, and dependency counts line up. Boundaries are weak where a module spans many folders, participates in cycles, or has high coupling.

## 7. External Dependency Risk

External dependency risk is derived from `external-boundary-pack.json`, module risk references, and dependency evidence. Modules marked `review` in the table have associated risk IDs or dependency evidence that should be checked before extraction.

## 8. Suggested Migration Order

1. PublicApi
2. SharedContracts
3. Verification
4. CrossCutting
5. Defer high-coupling/cyclic modules: Admin, ApplicationCore, Basket, Catalog, DataAccess, Identity, Order, Web

Human review is required before final sequencing because some call flows are partial and some module boundaries are candidate-only.
