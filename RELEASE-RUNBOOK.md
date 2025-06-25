# Release Runbook

## In between changes

- Update [CHANGELOG.md](CHANGELOG.md)
  - place changes under top header ``## **WORK IN PROGRESS**`` 
  - Never fill in a version, except when you create a new release.
  - add lines per change
  - you may refer to documentation using markdown links
  - use emoji's when you're enthousiastic


## Create new release

- Bump version in [_version.py](_version.py) See which kind of version below.

| Please choose a version                  | Version description                                                           |
|:-----------------------------------------|:------------------------------------------------------------------------------|
|   1.0.0 (major)                          | Breaking changes were introduced. This may include new features and bugfixes. |
|   0.20.0 (minor)                         | A new feature was added without breaking things. This may include bugfixes.   |
| ▸ 0.19.6 (patch)                         | A bug was fixed without adding new functionality.                             |
|   0.19.6-alpha.0 or similar (prerelease) | Bump an existing prerelease suffix, behaves like prepatch otherwise.          |
|   10.0.0-alpha.0 or similar (premajor)   | To provide test versions before a major release.                              |
|   0.20.0-alpha.0 or similar (preminor)   | To provide test versions before a minor release.                              |
|   0.19.6-alpha.0 or similar (prepatch)   | To provide test versions before a patch release.                              |

- Update [CHANGELOG.md](CHANGELOG.md)
  - use git log to add forgotten changes
  - Copy `## **WORK IN PROGRESS**` and change new header to `## vX.X.X (2025-12-31)`

- commit everything which is dirty

- create version tag `git tag vX.X.X`

- push tag `git push --tags`

- In https://github.com/wearetechnative/croctalk create release from newly made tag.
