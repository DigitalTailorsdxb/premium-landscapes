# Budget-Based Design Mode - Mock Data Example

## Scenario: "Not sure what you want? Let us design within your budget!"

This example shows the exact JSON payload sent to n8n when a customer chooses **budget-based design mode** instead of selecting specific materials.

---

## Customer Story

**Sarah Thompson** from Birmingham wants a complete garden redesign but isn't sure exactly what materials or features she wants. She knows:
- **Budget:** £25,000
- **Garden size:** 100m²
- **Requirements:** Low maintenance & pet friendly

Instead of picking individual materials (paving, decking, etc.), she checks the **"Not sure what you want? Let us design within your budget!"** checkbox and lets Premium Landscapes design the perfect garden within her budget constraints.

---

## The Data Flow

### 1. What the Customer Sees on the Quote Form

**Step 1:** Selects "Full Garden Redesign"

**Step 2:** Instead of selecting materials, she:
- ✅ Checks: "Not sure what you want? Let us design within your budget!"
- 📝 Types: "low maintenance & pet friendly" in the design vision notes

**Step 3:** Enters:
- Area: 100m² (slider)
- Budget: £25,000 (custom input field)

**Step 4:** Uploads photos, enters address

**Step 5:** Enters contact details and submits

---

### 2. What Gets Sent to n8n Webhook

```json
{
  "customer": {
    "name": "Sarah Thompson",
    "email": "sarah.thompson@example.com",
    "phone": "07712 345678",
    "postcode": "B15 2TT",
    "city": "Birmingham",
    "street": "Oak Avenue",
    "houseNumber": "42",
    "address": "42, Oak Avenue, Birmingham, B15 2TT, UK"
  },
  "project": {
    "title": "Full Garden Redesign at B15 2TT",
    "type": "full_garden_redesign",
    "totalArea_m2": 100,
    "totalBudget_gbp": 25000,
    "notes": "low maintenance & pet friendly",
    "gardenDesign": {
      "budgetBasedDesign": true,     // ← KEY FLAG
      "categories": {}                // ← EMPTY (no materials selected)
    }
  }
}
```

**Routing:** Automatically sent to → `/webhook/premium-landscapes-full-redesign`

---

### 3. How n8n Should Handle This

#### Detection Logic
```javascript
// Check if budget-based design mode
const isBudgetBased = project.gardenDesign.budgetBasedDesign === true;
const hasNoMaterials = Object.keys(project.gardenDesign.categories).length === 0;

if (isBudgetBased && hasNoMaterials) {
  // Customer wants you to design within their budget
  // Use AI to create design proposal
}
```

#### GPT-4 Prompt Example
```
Customer Requirements:
- Budget: £25,000
- Garden Size: 100m²
- Requirements: low maintenance & pet friendly
- Location: Birmingham (B15 2TT)

Create a comprehensive garden design proposal that:
1. Maximizes value within £25,000 budget
2. Requires minimal maintenance
3. Is safe and enjoyable for pets
4. Suits Birmingham climate
5. Provides itemized breakdown with:
   - Paving/hard landscaping
   - Lawn/planting
   - Boundaries
   - Features
   - Installation costs

Return JSON with materials, quantities, and pricing.
```

#### PDF Quote Generation
The n8n workflow should generate a PDF that includes:

**"Budget-Based Design Proposal"** section showing:
- Recommended materials with rationale
- Layout suggestions
- Phased approach options (if applicable)
- Professional design renders (optional)
- Why each element was chosen (low maintenance, pet-safe, etc.)

---

## Key Benefits for Customer

### Traditional Quote Flow
❌ Customer must know exactly what they want  
❌ Risk of choosing incompatible materials  
❌ May over/under-specify  

### Budget-Based Design Flow
✅ Trust the experts to design optimally  
✅ Get professional material recommendations  
✅ Designs optimized for budget  
✅ Perfect for indecisive customers  

---

## Technical Details

### Flag Behavior

| Scenario | `budgetBasedDesign` | `categories` | Interpretation |
|----------|-------------------|--------------|----------------|
| Customer selects materials | `false` | `{paving: [...], lawn: [...]}` | Standard full redesign with specific materials |
| Budget-based design | `true` | `{}` | Let Premium Landscapes design within budget |
| Mixed (edge case) | `true` | `{paving: [...]}` | Customer wants some materials + design the rest |

### Validation Rules
- ✅ Budget is **mandatory** for full redesign
- ✅ Minimum budget: £1,000
- ✅ Area must be provided
- ✅ Customer notes captured in `project.notes`

---

## Files Reference

- **Mock Data (JSON):** `MOCK_BUDGET_BASED_DESIGN.json`
- **Mock Data (n8n Code Node):** `N8N_MOCK_DATA_CODE.js` ← **Use this for n8n!**
- **Quote Engine:** `scripts/quote-engine.js`
- **Full Redesign Workflow Spec:** `N8N_FULL_REDESIGN_WORKFLOW_PROMPT.md`
- **Webhook Routing:** `DUAL_WEBHOOK_ROUTING.md`
- **Feature Documentation:** `BUDGET_BASED_DESIGN_FEATURE.md`

---

## Next Steps for n8n Implementation

1. **Import this JSON into n8n** to test the workflow
2. **Add GPT-4 node** that creates design proposal based on:
   - Budget (`totalBudget_gbp`)
   - Area (`totalArea_m2`)
   - Requirements (`project.notes`)
   - Location (`customer.postcode`)
3. **Generate PDF** with design proposal and itemized quote
4. **Send email** with PDF to customer
5. **Log to CRM** with "budget_based_design" tag for follow-up

---

✅ **This mock data is ready to paste into n8n for testing the budget-based design workflow!**
