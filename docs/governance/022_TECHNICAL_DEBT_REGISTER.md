# 022 Technical Debt Register

Every architectural compromise, deferred implementation, and "hack" must be documented here. Technical debt must not exist solely in the memory of the engineers.

| ID | Description | Impact | Introduced | Resolution Strategy | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TD-001** | Ray Windows Wheel Compatibility | `uv sync` fails on Windows for `ray>=2.10.0` under Python 3.11+. The core platform requires Ray, but local Windows dev environments are blocked. | M1 | Use environment markers (`sys_platform != 'win32'`) for local dev, mock Ray for local tests, and mandate Linux (WSL2/DevContainers) for full execution. | **OPEN** |
| **TD-002** | Local CI/CD Simulation | We currently rely on local pre-commit hooks and manual `pytest` rather than a fully provisioned remote GitHub Actions runner due to bootstrapping phase. | M1 | Stand up a formal GitHub repo with branch protections requiring the `ci.yml` matrix to pass. | **OPEN** |
