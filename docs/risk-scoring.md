# Risk Scoring Methodology

Each dependency receives a risk score from 0-100:

## Scoring Factors

| Factor | Points |
|--------|--------|
| Critical CVE | +30 |
| High CVE | +20 |
| Medium CVE | +10 |
| Abandoned (2+ years) | +25 |
| Blocked License | +40 |

## Risk Levels

- 0-20: Low (green)
- 21-40: Medium (yellow)
- 41-60: High (orange)
- 61-80: Critical (red)
- 81-100: Severe (block)