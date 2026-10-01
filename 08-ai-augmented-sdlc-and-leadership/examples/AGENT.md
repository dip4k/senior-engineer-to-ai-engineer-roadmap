# Repository Agent Guidelines: Order & Payment Microservice

> **Open Specification Standard**: Conforms to the Linux Foundation `AGENTS.md` standard. In multi-agent environments, symlink this file to both `AGENTS.md` and `CLAUDE.md` (`ln -s AGENT.md AGENTS.md && ln -s AGENT.md CLAUDE.md`).
>
> This document defines operational instructions, architectural invariants, and verification gates for autonomous coding agents operating within this repository. Keeps total lines under 100 to prevent attention dilution.

---

## 1. Environment & Build Commands
- **Runtime**: .NET 9 SDK (v9.0.100+) / C# 13 / PostgreSQL 16
- **Build Solution**: `dotnet build OrderService.sln --configuration Release /warnaserror`
- **Run Unit Tests**: `dotnet test tests/OrderService.UnitTests/OrderService.UnitTests.csproj --logger "console;verbosity=normal"`
- **Run Integration Tests**: `dotnet test tests/OrderService.IntegrationTests/OrderService.IntegrationTests.csproj` (requires local Docker daemon for Testcontainers)
- **Format & Lint**: `dotnet format --verify-no-changes`

---

## 2. Non-Negotiable Architectural Invariants
1. **Hexagonal Layer Separation**:
   - `OrderService.Domain`: ZERO external dependencies. Contains pure domain entities, value objects, and domain events. Never reference EF Core or ASP.NET packages here.
   - `OrderService.Application`: Contains MediatR commands, queries, and business use cases. References Domain only.
   - `OrderService.Infrastructure`: Implements persistence, external APIs, and message brokers. References Application and Domain.
   - `OrderService.Api`: Presentation minimal APIs and middleware. References Application and Infrastructure.
2. **Deterministic Typing**:
   - `<Nullable>enable</Nullable>` is enforced across all projects. No warnings tolerated.
   - Never use `dynamic`, untyped objects, or reflection for data mapping.
3. **Immutability & Value Objects**:
   - Use C# `record` for all DTOs, Commands, Queries, and Value Objects.
   - State mutations on Domain Entities must occur through explicit methods returning `Result<T>` or raising domain events.
4. **Data Access & Idempotency**:
   - All state-altering HTTP endpoints (`POST`, `PUT`, `PATCH`) must enforce the `Idempotency-Key` HTTP header.
   - Never write raw unparameterized SQL strings. All queries must utilize EF Core with compiled queries or strongly typed Dapper queries with explicit parameter mapping.

---

## 3. Allowed Dependencies & Tooling
- **Validation**: `FluentValidation` (v11.x)
- **Object Mapping**: Explicit extension methods or `Mapperly` (Source-generated). Do NOT introduce AutoMapper.
- **Testing**: `xUnit`, `FluentAssertions`, `Moq`, `Testcontainers.PostgreSql`.
- **JSON Serialization**: `System.Text.Json` (Source generated where applicable). Do NOT add `Newtonsoft.Json`.

---

## 4. Execution Workflow for Agents
When assigned an issue or feature implementation:
1. **Explore**: Read the relevant domain entities and existing test suites before modifying code.
2. **Test First (TDD)**: Add failing unit tests in `OrderService.UnitTests` covering both happy-path and boundary edge cases.
3. **Implement**: Write minimal, clean code to satisfy the tests while strictly honoring the hexagonal layer boundaries.
4. **Verify**: Execute `dotnet test` locally and verify that ALL tests pass.
5. **Lint Check**: Run `dotnet format --verify-no-changes` to ensure zero style deviations.
6. **Report**: Summarize changes, citing modified files and test execution output.
