# Architecture Pattern Report

## 1. Detected Architecture Pattern

Detected pattern: Layered Monolith.

## 2. Evidence

- Candidate pattern evidence from layering pack: [
  {
    "pattern": "Layered Monolith",
    "evidence": "Multiple projects/layers detected within one solution/repository and shared deployable units.",
    "confidence": 0.78
  },
  {
    "pattern": "Clean Architecture",
    "evidence": "Parsed layers include application/domain/infrastructure-style components; project names are used only as supporting evidence.",
    "confidence": 0.66
  },
  {
    "pattern": "Modular Monolith",
    "evidence": "Multiple module candidates exist inside shared backend/frontend projects; service separation is not established by evidence packs.",
    "confidence": 0.52
  }
]
- System inventory detects 2 deployable unit candidates and 10 project records.
- Component evidence detects layers across Presentation/UI, API, Application, Domain, Infrastructure, DataAccess, Integration, CrossCutting, and Unknown.

Source file anchors:

- src/ApplicationCore/ApplicationCore.csproj
- src/BlazorAdmin/BlazorAdmin.csproj
- src/BlazorShared/BlazorShared.csproj
- src/Infrastructure/Infrastructure.csproj
- src/PublicApi/PublicApi.csproj
- src/Web/Web.csproj
- tests/FunctionalTests/FunctionalTests.csproj
- tests/IntegrationTests/IntegrationTests.csproj

## 3. Layer Structure

- API: 17 components
- Application: 69 components
- CrossCutting: 62 components
- DataAccess: 15 components
- Domain: 18 components
- Infrastructure: 9 components
- Integration: 2 components
- Presentation/UI: 115 components
- Unknown: 3 components

## 4. Pattern Confidence

Primary pattern confidence is 0.78. Competing pattern candidates and confidence scores are shown in the evidence block above, so this is an evidence-bounded observation rather than a pure pattern claim.

## 5. Pattern Violations

- ARCH-VIOL-001: Controller-like component CatalogBrandListEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-002: Controller-like component CatalogItemGetByIdEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-003: Controller-like component CreateCatalogItemEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-004: Controller-like component DeleteCatalogItemEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-005: Controller-like component UpdateCatalogItemEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-006: Controller-like component CatalogTypeListEndpoint depends directly on repository EfRepository.
- ARCH-VIOL-007: Controller-like component IndexModel depends directly on repository EfRepository.
- ARCH-VIOL-008: Module dependency cycle detected: Admin -> ApplicationCore -> Basket -> Catalog -> DataAccess -> Identity -> Order -> Web
- ARCH-VIOL-009: Component EfRepository has high coupling score 16.
- ARCH-VIOL-010: Component UriComposer has high coupling score 8.

Violation source anchors: src/PublicApi/CatalogBrandEndpoints/CatalogBrandListEndpoint.cs, src/PublicApi/CatalogItemEndpoints/CatalogItemGetByIdEndpoint.cs, src/PublicApi/CatalogItemEndpoints/CreateCatalogItemEndpoint.cs, src/PublicApi/CatalogItemEndpoints/DeleteCatalogItemEndpoint.cs, src/PublicApi/CatalogItemEndpoints/UpdateCatalogItemEndpoint.cs, src/PublicApi/CatalogTypeEndpoints/CatalogTypeListEndpoint.cs, src/Web/Pages/Basket/Index.cshtml.cs, architecture-output/evidence-packs/dependency-pack.json. Dependency-cycle and high-coupling claims are derived from `architecture-output/evidence-packs/dependency-pack.json`, which preserves source-file evidence for the underlying component and module dependency candidates.

## 6. What This Means For Reverse Engineering

Reverse engineering should preserve the project/layer split in the evidence model and treat module boundaries as candidates, not confirmed bounded contexts. Repository sharing and module cycles should be analyzed before deriving modernization slices.

## 7. What This Means For Forward Engineering

Forward engineering should preserve externally visible API behavior and important UI flows, but should not copy direct UI/API-to-data-access dependencies or unresolved module cycles. The future design should clarify candidate module boundaries and data-access ownership first.
