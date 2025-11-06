// Premium Landscapes — Full Redesign (Mock Payload)
// Emits a single item with the website-equivalent payload shape.

const payload = {
  customer: {
    name: "Sarah Thompson",
    email: "sarah.thompson@example.com",
    phone: "07712 345678",
    postcode: "B15 2TT",
    city: "Birmingham",
    street: "Oak Avenue",
    houseNumber: "42",
    address: "42, Oak Avenue, Birmingham, B15 2TT, UK"
  },
  project: {
    title: "Full Garden Redesign at B15 2TT",
    type: "full_garden_redesign",
    totalArea_m2: 100,
    totalBudget_gbp: 25000,
    layoutType: "standard",
    sunlight: "partial sun",
    stylePreference: "contemporary",
    maintenanceLevel: "low maintenance",
    siteConditions: {
      access: "standard access",
      soilType: "loam",
      drainage: "good"
    },
    products: [],
    extras: {
      pergola: { include: false },
      firePit: { include: false },
      waterFeature: { include: false }
    },
    notes: "low maintenance & pet friendly",
    gardenDesign: {
      budgetBasedDesign: true,
      categories: {}
    }
  },
  metadata: {
    source: "website_quote_form",
    timestamp: "2025-11-05T17:00:00Z",
    quoteType: "full_garden_redesign",
    webhookDestination: "https://n8n.example.com/webhook/premium-landscapes-full-redesign"
  }
};

return [{ json: payload }];
