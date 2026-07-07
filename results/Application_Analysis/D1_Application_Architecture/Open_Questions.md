# Open Questions — eShopOnWeb Architecture Extraction

## Purpose

This document records questions that could not be answered from the available Layer 1 source artifacts. Each question identifies the impacted analysis and what additional evidence is needed to resolve it.

---

## Category: Web Project (Critical — Primary User Flow Unknown)

| ID | Question | Why Unknown | Impact | Evidence Needed |
|---|---|---|---|---|
| OQ-001 | What controllers and Razor Pages exist in the Web project? | Web/Controllers/ and Web/Pages/ source files were not present in Layer 1 artifacts | All primary user-facing routes (catalog browse, basket, checkout, order history) are unknown | Read Web/Controllers/ and Web/Pages/ directory recursively |
| OQ-002 | Does the Web project use cookie-based ASP.NET Identity or redirect to JWT? | Web project Startup/Program.cs not in Layer 1 | Authentication strategy for the storefront is unknown | Read src/Web/Program.cs, src/Web/Startup.cs |
| OQ-003 | How is the basket controller bound to the authenticated user? | Web basket controller not visible | Price manipulation risk (RISK-006) cannot be confirmed or dismissed | Read basket-related Web controller |
| OQ-004 | What triggers basket deletion after a successful order? | OrderService.CreateOrderAsync does not delete basket | Data integrity risk (RISK-004) impact unclear | Read checkout controller in Web project |
| OQ-005 | What routes serve catalog browsing (list, filter, detail) for anonymous shoppers? | Web controllers not in Layer 1 | Catalog read flow for non-admin users is undocumented | Read CatalogController or equivalent in Web project |

---

## Category: PublicApi Catalog Endpoints (High — Admin Security Unknown)

| ID | Question | Why Unknown | Impact | Evidence Needed |
|---|---|---|---|---|
| OQ-006 | Is POST api/catalog-items protected by [Authorize(Roles=Administrators)]? | CatalogItemEndpoints/ source not in Layer 1 | If unprotected, any authenticated user can create catalog items | Read src/PublicApi/CatalogItemEndpoints/Create.cs or equivalent |
| OQ-007 | Is PUT api/catalog-items protected by admin role? | Same as above | Unauthorized item modification possible | Read src/PublicApi/CatalogItemEndpoints/Update.cs |
| OQ-008 | Is DELETE api/catalog-items/{id} protected by admin role? | Same as above | Unauthorized item deletion possible | Read src/PublicApi/CatalogItemEndpoints/Delete.cs |
| OQ-009 | What does GET api/catalog-items return — all items or paginated? | Endpoint source not in Layer 1 | Performance characteristics unknown | Read CatalogItemListEndpoint; check for PageSize/Page params |
| OQ-010 | Does POST api/catalog-items handle image storage? CreateCatalogItemRequest has PictureBase64 | Endpoint source not in Layer 1 | Media handling strategy unknown; base64 uploads have size limits | Read CreateEndpoint; check for file storage logic |

---

## Category: Identity and Authentication

| ID | Question | Why Unknown | Impact | Evidence Needed |
|---|---|---|---|---|
| OQ-011 | What GET /User endpoint does CustomAuthStateProvider call? | Endpoint not found in PublicApi or Web Layer 1 artifacts | Auth state flow incomplete | Search for UserController or UserEndpoint in Web/PublicApi |
| OQ-012 | Is the Web project's cookie auth session independent from BlazorAdmin's JWT auth? | Web auth middleware not visible | Identity extraction plan cannot finalize | Read src/Web/Program.cs authentication config |
| OQ-013 | Are there roles other than 'Administrators'? | Only AuthorizationConstants.Roles.ADMINISTRATORS visible | Authorization model incomplete | Read AuthorizationConstants.cs fully; search for other role usages |

---

## Category: Deployment and Infrastructure

| ID | Question | Why Unknown | Impact | Evidence Needed |
|---|---|---|---|---|
| OQ-014 | Is BlazorAdmin embedded within the Web project (hosted mode) or deployed as a standalone SPA? | BlazorAdmin wwwroot/appsettings.json baseUrls.webBase = '/' suggests co-hosting but is ambiguous | BlazorAdmin deployment architecture unknown | Check Web project .csproj for BlazorAdmin reference; read Web Program.cs for UseBlazorFrameworkFiles |
| OQ-015 | Is there an Azure DevOps or GitHub Actions CI/CD pipeline defined? | No .github/ or .azure/pipelines/ directory visible in Layer 1 artifacts | Deployment modernization scope unknown | Check .github/workflows/ and .azure/pipelines/ |
| OQ-016 | Are catalog images stored locally (wwwroot) or in Azure Blob Storage? | UriComposer replaces a placeholder but destination URL unknown | Catalog image handling in microservice extraction unclear | Read src/Web/wwwroot/images/ presence; check CatalogSettings.cs |
| OQ-017 | What is the azure.yaml infra provisioning scope? Does it provision Redis, Service Bus, or only App Service + SQL? | azure.yaml lists only web and api as services | Azure infrastructure baseline unknown | Read infra/ bicep files (infra/main.bicep) |

---

## Category: Domain Model

| ID | Question | Why Unknown | Impact | Evidence Needed |
|---|---|---|---|---|
| OQ-018 | Are Buyer and PaymentMethod entities genuinely dead code, or are they used by the Web project? | No service or repository references visible in Layer 1; web project not scanned | Dead code risk assessment (VIO-008) may be incorrect | Read Web project — search for IBuyerRepository or PaymentMethod usage |
| OQ-019 | Is there an order status lifecycle (Pending, Processing, Shipped, Delivered, Cancelled)? | Order entity has no Status field in visible artifacts | Business process completeness unknown | Read Order.cs fully; check for any OrderStatus enum |
| OQ-020 | Is there any email-triggered event (order confirmation, password reset)? | EmailSender is a stub; callers not visible | Feature completeness and stub impact unknown | Search Web project for IEmailSender injection |

---

## Category: Testing

| ID | Question | Why Unknown | Impact | Evidence Needed |
|---|---|---|---|---|
| OQ-021 | Does the project have unit or integration tests? | Test project source files not in Layer 1 artifacts | Test coverage baseline unknown for forward engineering | Check for tests/ or *.Tests.csproj projects |
| OQ-022 | Are there functional/E2E tests (Playwright, Selenium)? | No test artifacts in Layer 1 | QA strategy for migration unknown | Check functional tests directory |
