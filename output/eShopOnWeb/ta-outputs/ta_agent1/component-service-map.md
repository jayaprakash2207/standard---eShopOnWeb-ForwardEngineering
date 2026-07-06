## Component & Service Map

| Service / Component Name | Type | Exposed Port(s) | Communication Protocol(s) | Primary Technology | Source File | Notes |
|---|---|---|---|---|---|---|
| eshopwebmvc (Web) | API Service / Frontend App (ASP.NET Core MVC + Razor + Blazor Server host) | Container: 8080 (env ASPNETCORE_URLS); Host mapping 5106:8080; Dev: https://localhost:44315 | HTTP / HTTPS | .NET 8.0, ASP.NET Core MVC, Blazor Server hosting | src/Web/Dockerfile, docker-compose.yml, docker-compose.override.yml | depends_on: sqlserver (docker-compose.yml) |
| eshoppublicapi (PublicApi) | API Service (REST, Swagger-documented) | Dockerfile EXPOSE 80, 443; Container runtime: 8080 (env ASPNETCORE_URLS); Host mapping 5200:8080; Dev: https://localhost:5099 | HTTP / HTTPS | .NET 8.0, ASP.NET Core Web API, Swashbuckle | src/PublicApi/Dockerfile, docker-compose.yml, docker-compose.override.yml | LOW - Dockerfile EXPOSE (80/443) differs from compose port mapping (8080); depends_on: sqlserver |
| sqlserver | Database (Container) | 1433 (mapped 1433:1433) | TCP / TDS (SQL) | Azure SQL Edge (SQL Server-compatible) | docker-compose.yml | Provisioned for both eshopwebmvc and eshoppublicapi |
| BlazorAdmin | Frontend App (Blazor WebAssembly, served via Web host) | N/A (hosted, no direct container port) | HTTP / HTTPS | Blazor WebAssembly (.NET 8.0) | src/BlazorAdmin/BlazorAdmin.csproj, src/BlazorAdmin/wwwroot/appsettings*.json | Communicates with PublicApi (apiBase) and Web (webBase) per environment config |
| ApplicationCore | Class Library (domain/application layer) | N/A | N/A (in-process) | .NET 8.0 class library | src/ApplicationCore/ApplicationCore.csproj | Referenced by Infrastructure, PublicApi, Web (via project references) |
| BlazorShared | Class Library (shared models/validation) | N/A | N/A (in-process) | .NET class library, FluentValidation | src/BlazorShared/BlazorShared.csproj | Referenced by ApplicationCore and BlazorAdmin |
| Infrastructure | Class Library (data access / EF Core / Identity) | N/A | N/A (in-process) | EF Core (SQL Server, PostgreSQL, InMemory providers) | src/Infrastructure/Infrastructure.csproj | Referenced by PublicApi and Web |
| FunctionalTests | Test Project (in-process host via WebApplicationFactory) | N/A | N/A | xunit, Microsoft.AspNetCore.Mvc.Testing, EF Core InMemory | tests/FunctionalTests/FunctionalTests.csproj | References ApplicationCore, PublicApi, Web |
| IntegrationTests | Test Project | N/A | N/A | xunit, NSubstitute, EF Core InMemory | tests/IntegrationTests/IntegrationTests.csproj | References Infrastructure, UnitTests |
| UnitTests | Test Project | N/A | N/A | xunit, NSubstitute | tests/UnitTests/UnitTests.csproj | References ApplicationCore, Web |
| PublicApiIntegrationTests | Test Project (in-process host via WebApplicationFactory) | N/A | N/A | MSTest, Microsoft.AspNetCore.Mvc.Testing, coverlet | tests/PublicApiIntegrationTests/PublicApiIntegrationTests.csproj | References PublicApi, Web; uses `UseOnlyInMemoryDatabase: true` (appsettings.test.json) |

---

### Chunk Inventory - Component & Service Map
- Technology components found this chunk: ASP.NET Core MVC, ASP.NET Core Web API, Blazor WebAssembly, Azure SQL Edge
- Data stores found this chunk: sqlserver (Azure SQL Edge, see Data Store Registry)
- Integrations found this chunk: BlazorAdmin -> PublicApi (apiBase), BlazorAdmin -> Web (webBase)
- Infrastructure resources found: eshopwebmvc container, eshoppublicapi container, sqlserver container
- Environments identified: Development, Docker, Production/default (see Infrastructure & Deployment Blueprint)
- Cross-layer dependencies flagged: eshopwebmvc and eshoppublicapi both depend_on sqlserver (Data Layer); BlazorAdmin depends on PublicApi and Web base URLs (Application Layer)
- Newly flagged as SHARED COMPONENT: None new this chunk
- LOW CONFIDENCE items raised this chunk: PublicApi Dockerfile EXPOSE (80/443) conflicts with docker-compose port mapping (8080) - Agent 2 to resolve actual listening port
