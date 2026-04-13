# Data Generation

## Overview

Python script using **Faker** to generate realistic test data for cosmetics database.

## Usage

**With Makefile (recommended):**

```bash
make generate-data
```

**Manual:**

```bash
podman exec ibm-blueboard-backend python scripts/generate_fake_data.py
```

## Generated Data

| Entity       | Count | Description                        |
| ------------ | ----- | ---------------------------------- |
| Products     | 100   | 6 categories, 10+ brands, €10-€150 |
| Customers    | 500   | 5 segments, 13 French regions      |
| Sales        | 2,500 | 12 months, 4 channels              |
| Satisfaction | 1,200 | 5-star ratings, comments           |
| Inventory    | 100   | Stock levels                       |
| Returns      | 150   | Return reasons and statuses        |
| Promotions   | 30    | Discount campaigns                 |

## Features

- **Realistic**: French names, addresses, product descriptions
- **Relationships**: Maintains FK constraints
- **Variety**: Random distributions for ratings, segments, channels
- **Time-based**: Sales spread over 12 months

**Warning**: Clears all existing data before generation. Development/testing only.

## Script Location

`backend/scripts/generate_fake_data.py`
