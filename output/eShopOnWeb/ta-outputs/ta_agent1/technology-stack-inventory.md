## Technology Stack Inventory

| Component Name | Version | Category | Layer | Package Manager / Source | Source File | Confidence |
|---|---|---|---|---|---|---|
| .NET SDK/Runtime | 8.0.x | Runtime / SDK | Build | dotnet CLI | .github/workflows/dotnetcore.yml | HIGH |
| mcr.microsoft.com/dotnet/sdk | 8.0 | Container Base Image (build stage) | Build | Docker Hub (MCR) | src/Web/Dockerfile, src/PublicApi/Dockerfile | HIGH |
| mcr.microsoft.com/dotnet/aspnet | 8.0 | Container Base Image (runtime stage) | Infrastructure | Docker Hub (MCR) | src/Web/Dockerfile, src/PublicApi/Dockerfile | HIGH |
| mcr.microsoft.com/azure-sql-edge | (not declared / latest) | Container Base Image / Database | Data | Docker Hub (MCR) | docker-compose.yml | LOW - no tag declared, defaults to latest |
| Microsoft.NET.Sdk.Web | (project SDK, no version) | Web App SDK | Application | NuGet/MSBuild SDK | src/Web/Web.csproj, src/PublicApi/PublicApi.csproj | HIGH |
| Microsoft.NET.Sdk.BlazorWebAssembly | (project SDK, no version) | Frontend Framework SDK | Application | NuGet/MSBuild SDK | src/BlazorAdmin/BlazorAdmin.csproj | HIGH |
| Ardalis.GuardClauses | (not declared) | Guard Clause Library | Application | nuget | src/ApplicationCore/ApplicationCore.csproj | LOW - VERSION UNKNOWN, central package mgmt (Directory.Packages.props referenced but not provided) |
| Ardalis.Result | (not declared) | Result/Outcome Library | Application | nuget | src/ApplicationCore/ApplicationCore.csproj | LOW - VERSION UNKNOWN |
| Ardalis.Specification | (not declared) | Specification Pattern Library | Application | nuget | src/ApplicationCore/ApplicationCore.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN |
| System.Security.Claims | (not declared) | Identity/Claims Library | Security | nuget | src/ApplicationCore/ApplicationCore.csproj | LOW - VERSION UNKNOWN |
| System.Text.Json | (not declared) | JSON Serialization | Application | nuget | src/ApplicationCore/ApplicationCore.csproj | LOW - VERSION UNKNOWN |
| Blazored.LocalStorage | (not declared) | Browser Storage Library | Application | nuget | src/BlazorAdmin/BlazorAdmin.csproj | LOW - VERSION UNKNOWN |
| BlazorInputFile | (not declared) | File Upload Component | Application | nuget | src/BlazorAdmin/BlazorAdmin.csproj, src/BlazorShared/BlazorShared.csproj | LOW - VERSION UNKNOWN |
| Microsoft.AspNetCore.Components.Authorization | (not declared) | Auth Components | Security | nuget | src/BlazorAdmin/BlazorAdmin.csproj | LOW - VERSION UNKNOWN |
| Microsoft.AspNetCore.Components.WebAssembly | (not declared) | Blazor WASM Framework | Application | nuget | src/BlazorAdmin/BlazorAdmin.csproj | LOW - VERSION UNKNOWN |
| Microsoft.AspNetCore.Components.WebAssembly.Authentication | (not declared) | Blazor WASM Auth | Security | nuget | src/BlazorAdmin/BlazorAdmin.csproj | LOW - VERSION UNKNOWN |
| Microsoft.AspNetCore.Components.WebAssembly.DevServer | (not declared) | Blazor WASM Dev Server | Build | nuget | src/BlazorAdmin/BlazorAdmin.csproj | LOW - VERSION UNKNOWN |
| Microsoft.Extensions.Identity.Core | (not declared) | Identity Core Library | Security | nuget | src/BlazorAdmin/BlazorAdmin.csproj | LOW - VERSION UNKNOWN |
| Microsoft.Extensions.Logging.Configuration | (not declared) | Logging Configuration | Observability | nuget | src/BlazorAdmin/BlazorAdmin.csproj | LOW - VERSION UNKNOWN |
| System.Net.Http.Json | (not declared) | HTTP/JSON Client Extensions | Application | nuget | src/BlazorAdmin/BlazorAdmin.csproj | LOW - VERSION UNKNOWN |
| FluentValidation | (not declared) | Validation Library | Application | nuget | src/BlazorShared/BlazorShared.csproj | LOW - VERSION UNKNOWN |
| Ardalis.Specification.EntityFrameworkCore | (not declared) | ORM Specification Extension | Data | nuget | src/Infrastructure/Infrastructure.csproj | LOW - VERSION UNKNOWN |
| Microsoft.AspNetCore.Identity.EntityFrameworkCore | (not declared) | Identity ORM Provider | Security | nuget | src/Infrastructure/Infrastructure.csproj, src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Microsoft.EntityFrameworkCore.InMemory | (not declared) | ORM In-Memory Provider | Data | nuget | src/Infrastructure/Infrastructure.csproj, src/PublicApi/PublicApi.csproj, src/Web/Web.csproj, tests/FunctionalTests/FunctionalTests.csproj, tests/IntegrationTests/IntegrationTests.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Npgsql.EntityFrameworkCore.PostgreSQL | (not declared) | ORM PostgreSQL Provider | Data | nuget | src/Infrastructure/Infrastructure.csproj | LOW - VERSION UNKNOWN |
| System.IdentityModel.Tokens.Jwt | (not declared) | JWT Token Library | Security | nuget | src/Infrastructure/Infrastructure.csproj, src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Ardalis.ApiEndpoints | (not declared) | API Endpoint Pattern Library | Application | nuget | src/PublicApi/PublicApi.csproj | LOW - VERSION UNKNOWN |
| AutoMapper.Extensions.Microsoft.DependencyInjection | (not declared) | Object Mapping Library | Application | nuget | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| MinimalApi.Endpoint | (not declared) | Minimal API Pattern Library | Application | nuget | src/PublicApi/PublicApi.csproj | LOW - VERSION UNKNOWN |
| Swashbuckle.AspNetCore | (not declared) | OpenAPI/Swagger Generator | Application | nuget | src/PublicApi/PublicApi.csproj | LOW - VERSION UNKNOWN |
| Swashbuckle.AspNetCore.SwaggerUI | (not declared) | OpenAPI/Swagger UI | Application | nuget | src/PublicApi/PublicApi.csproj | LOW - VERSION UNKNOWN |
| Swashbuckle.AspNetCore.Annotations | (not declared) | OpenAPI Annotations | Application | nuget | src/PublicApi/PublicApi.csproj | LOW - VERSION UNKNOWN |
| Microsoft.AspNetCore.Authentication.JwtBearer | (not declared) | JWT Bearer Auth Middleware | Security | nuget | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore | (not declared) | EF Core Diagnostics | Data | nuget | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Microsoft.AspNetCore.Identity.UI | (not declared) | Identity UI Scaffolding | Security | nuget | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Microsoft.EntityFrameworkCore.SqlServer | (not declared) | ORM SQL Server Provider | Data | nuget | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Microsoft.EntityFrameworkCore.Tools | (not declared) | EF Core CLI/Design Tools | Build | nuget | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Microsoft.VisualStudio.Azure.Containers.Tools.Targets | (not declared) | Container Tooling for VS | Build | nuget | src/PublicApi/PublicApi.csproj | LOW - VERSION UNKNOWN |
| Microsoft.VisualStudio.Web.CodeGeneration.Design | (not declared) | Scaffolding/Code Generation | Build | nuget | src/PublicApi/PublicApi.csproj, src/Web/Web.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Ardalis.ListStartupServices | (not declared) | Startup Diagnostics Library | Observability | nuget | src/Web/Web.csproj | LOW - VERSION UNKNOWN |
| Azure.Extensions.AspNetCore.Configuration.Secrets | (not declared) | Azure Key Vault Config Provider | Security | nuget | src/Web/Web.csproj | LOW - VERSION UNKNOWN |
| Azure.Identity | (not declared) | Azure Identity/Auth SDK | Security | nuget | src/Web/Web.csproj | LOW - VERSION UNKNOWN |
| MediatR | (not declared) | Mediator/CQRS Library | Application | nuget | src/Web/Web.csproj | LOW - VERSION UNKNOWN |
| BuildBundlerMinifier | (not declared) | CSS/JS Bundler & Minifier | Build | nuget | src/Web/Web.csproj (Release configuration only) | LOW - VERSION UNKNOWN |
| Microsoft.AspNetCore.Components.WebAssembly.Server | (not declared) | Blazor Server Hosting for WASM | Application | nuget | src/Web/Web.csproj | LOW - VERSION UNKNOWN |
| Microsoft.Web.LibraryManager.Build | (not declared) | Client-side Library Manager (libman) | Build | nuget | src/Web/Web.csproj | LOW - VERSION UNKNOWN |
| Microsoft.AspNetCore.Mvc.Testing | (not declared) | Integration Test Host | Build | nuget | tests/FunctionalTests/FunctionalTests.csproj, tests/PublicApiIntegrationTests/PublicApiIntegrationTests.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| Microsoft.NET.Test.Sdk | (not declared) | Test SDK | Build | nuget | tests/FunctionalTests, tests/IntegrationTests, tests/PublicApiIntegrationTests, tests/UnitTests (*.csproj) | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| xunit | (not declared) | Test Framework | Build | nuget | tests/FunctionalTests/FunctionalTests.csproj, tests/IntegrationTests/IntegrationTests.csproj, tests/UnitTests/UnitTests.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| xunit.runner.visualstudio | (not declared) | Test Runner | Build | nuget | tests/FunctionalTests, tests/IntegrationTests, tests/UnitTests (*.csproj) | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| xunit.runner.console | (not declared) | Test Runner (console) | Build | nuget | tests/UnitTests/UnitTests.csproj | LOW - VERSION UNKNOWN |
| dotnet-xunit | 2.3.1 | Test CLI Tool | Build | nuget (DotNetCliToolReference) | tests/FunctionalTests/FunctionalTests.csproj | HIGH |
| NSubstitute | (not declared) | Mocking Library | Build | nuget | tests/IntegrationTests/IntegrationTests.csproj, tests/UnitTests/UnitTests.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| NSubstitute.Analyzers.CSharp | (not declared) | Mocking Analyzer | Build | nuget | tests/IntegrationTests/IntegrationTests.csproj, tests/UnitTests/UnitTests.csproj | LOW - VERSION UNKNOWN - SHARED COMPONENT |
| MSTest.TestAdapter | (not declared) | Test Framework Adapter | Build | nuget | tests/PublicApiIntegrationTests/PublicApiIntegrationTests.csproj | LOW - VERSION UNKNOWN |
| MSTest.TestFramework | (not declared) | Test Framework | Build | nuget | tests/PublicApiIntegrationTests/PublicApiIntegrationTests.csproj | LOW - VERSION UNKNOWN |
| coverlet.collector | (not declared) | Code Coverage Collector | Build | nuget | tests/PublicApiIntegrationTests/PublicApiIntegrationTests.csproj | LOW - VERSION UNKNOWN |
| actions/checkout | v2 | CI/CD Action (source checkout) | CI-CD | github actions | .github/workflows/dotnetcore.yml, .github/workflows/richnav.yml | HIGH - SHARED COMPONENT |
| actions/setup-dotnet | v1 | CI/CD Action (.NET SDK setup) | CI-CD | github actions | .github/workflows/dotnetcore.yml, .github/workflows/richnav.yml | HIGH - SHARED COMPONENT |
| microsoft/RichCodeNavIndexer | v0.1 | CI/CD Action (code indexing) | CI-CD | github actions | .github/workflows/richnav.yml | HIGH |

---

### Carried Forward (Cumulative)
- Technology components: see table above (54 entries)
- Data stores: Azure SQL Edge / SQL Server (docker-compose.yml, appsettings.Docker.json), PostgreSQL (appsettings.json via Npgsql), EF Core InMemory (multiple csproj)
- Integrations: actions/checkout@v2, actions/setup-dotnet@v1, microsoft/RichCodeNavIndexer@v0.1, Azure Key Vault (Azure.Identity / Azure.Extensions.AspNetCore.Configuration.Secrets), Dependabot (nuget)
- LOW CONFIDENCE items: 47 (majority = VERSION UNKNOWN due to central package management file `Directory.Packages.props` referenced in eShopOnWeb.sln but not provided in scan input)
