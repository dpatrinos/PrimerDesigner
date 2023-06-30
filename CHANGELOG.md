# Changelog

## v0.2.0 (2023-06-30)

### Features

- Added `-p`/`--plus` and `-m`/`--minus` flags to allow for specification of (+) or (-) strand
- Added default value for `destination` (current working directory)
- Added specifications of strand and bases to the left and right of the intron to the output FASTA header
- Shortened `--bpLeft` and `--bpRight` flags to `--left` and `--right`, respectively
- Shortened `--startPos` and `--stopPos` flags to `--start` and `--stop`, respectively
- Shortened `--intronX` flag to `--intron`
- Shortened `--chromosome` flag to `--chr`
- Shortened `--sjDataset` flag to `--sj` (still accepts `-s`)
- Deprecated `--accVersion` flag in favor of sole use of `--chr` flag

### Documentation

- Revised README.md to reflect changes in v0.1.2

### Bug Fixes

- Resolved issue in sequence acquisition logic that affected an extremely small number of intron possibilities

## v0.1.1 (2023-06-12)

### Documentation

- Fixed inconsistencies in references to variable names
- Added CHANGELOG.md
- Added complete usage to README.md

## v0.1.0 (2023-06-11)

- First release of `PrimerDesigner`