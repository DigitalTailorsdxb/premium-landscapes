# AI Design Workflow - Payload Reference

## Overview
When a customer uploads a photo and requests AI garden designs, the JavaScript sends a structured payload to n8n containing the photo in Base64 format.

## Photo Upload Flow

### 1. Customer Action
- Customer checks "Also send me AI garden design concepts" in Step 5
- Upload section appears
- Customer uploads 1 photo (limited to single image)

### 2. JavaScript Processing
```javascript
// Priority: AI-specific photos (Step 5) > General photos (Step 4)
const photoSource = aiDesignFiles.length > 0 ? aiDesignFiles : quoteData.files;

// Convert to Base64
const file = photoSource[0];
const base64Data = await convertFileToBase64(file);

// Build photo object
photoObject = {
    name: file.name,           // "my-garden.jpg"
    type: file.type,           // "image/jpeg"
    size: file.size,           // 245678 (bytes)
    data: base64Data           // "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
};
```

### 3. Base64 Conversion
```javascript
function convertFileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (error) => reject(error);
        reader.readAsDataURL(file);  // Returns "data:image/jpeg;base64,..."
    });
}
```

## Complete Payload Structure

### With Photo Upload
```json
{
  "customer": {
    "email": "customer@example.com",
    "phone": "07444887813",
    "name": "John Smith"
  },
  "design": {
    "features": ["patio", "turf", "lighting"],
    "styleDescription": "Modern garden with patio and artificial turf",
    "gardenSize": "50",
    "budget": "£15,000",
    "materials": [
      {
        "category": "paving",
        "name": "porcelain-paving",
        "displayName": "Porcelain Paving"
      }
    ],
    "budgetBasedDesign": false,
    "designNotes": "Want a low-maintenance family garden"
  },
  "photo": {
    "name": "my-garden.jpg",
    "type": "image/jpeg",
    "size": 245678,
    "data": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
  },
  "metadata": {
    "timestamp": "2025-11-18T10:30:00.000Z",
    "source": "quote-form",
    "formVersion": "2.0",
    "quoteType": "full-redesign",
    "hasPhoto": true,
    "hasMaterials": true
  }
}
```

### Without Photo (Budget-Based Design)
```json
{
  "customer": {
    "email": "customer@example.com",
    "phone": "07444887813",
    "name": "Jane Doe"
  },
  "design": {
    "features": [],
    "styleDescription": "Budget-based design",
    "gardenSize": "75",
    "budget": "£25,000",
    "materials": [],
    "budgetBasedDesign": true,
    "designNotes": "Low maintenance, pet-friendly, sunny garden"
  },
  "photo": null,
  "metadata": {
    "timestamp": "2025-11-18T10:35:00.000Z",
    "source": "quote-form",
    "formVersion": "2.0",
    "quoteType": "full-redesign",
    "hasPhoto": false,
    "hasMaterials": false
  }
}
```

## Photo Priority Logic

### Scenario 1: AI-Specific Photo Uploaded (Step 5)
- User checks AI design checkbox → Upload section appears
- User uploads photo in Step 5 AI section
- **Result:** AI-specific photo is used (priority)

### Scenario 2: General Photo Uploaded (Step 4)
- User uploads photo in Step 4 (general upload)
- User checks AI design checkbox in Step 5
- **Result:** Step 4 photo is used (fallback)

### Scenario 3: No Photos Uploaded
- User checks AI design checkbox but uploads no photos
- **Result:** `photo: null`, workflow uses budget-based design

## n8n Workflow Usage

### With Photo (GPT-4o Vision)
```javascript
// In n8n Code node
const photoData = $json.photo?.data;

if (photoData) {
  // Photo is available - use GPT-4o Vision
  // Send base64 image to GPT-4o for analysis
  // Generate design based on actual garden photo
} else {
  // No photo - use GPT-4o Text
  // Generate design based on budget and requirements only
}
```

### Photo Mask (Future Enhancement)
Currently, the entire garden photo is processed. For future enhancement:
- Add mask drawing tool in UI
- User selects area to redesign
- Send both original photo + mask to n8n
- Workflow uses mask for targeted editing

## Testing

### Browser Console Output
When submitting with photo:
```
📤 Sending to AI Design workflow: https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-ai-design
📦 Design payload: {...}
📸 Photo details: {
  name: "garden-photo.jpg",
  type: "image/jpeg",
  size: "239.92 KB",
  dataPreview: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
}
✅ AI Design workflow triggered successfully
```

When submitting without photo:
```
📤 Sending to AI Design workflow: https://digitaltailorsdxb.app.n8n.cloud/webhook/premium-landscapes-ai-design
📦 Design payload: {...}
📸 No photo uploaded - will use budget-based design
✅ AI Design workflow triggered successfully
```

## Key Points

1. **Single Image Only:** Limited to 1 photo to prevent workflow confusion
2. **Base64 Format:** Full data URL with MIME type prefix included
3. **Complete Metadata:** name, type, size, and data all provided
4. **Priority Logic:** AI-specific uploads > General uploads > null
5. **Dual Mode:** Photo-based (GPT-4o Vision) OR Budget-based (GPT-4o Text)

## File Size Limits

- **Recommended:** < 5MB per image
- **Browser Limit:** ~10MB (base64 overhead)
- **n8n Limit:** Check your n8n instance payload size limits

Compress large images before upload for better performance.
