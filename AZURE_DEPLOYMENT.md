# Azure Deployment Guide - QDA Bilingual App

Complete guide to deploy the full-featured QDA application on Azure with document management, qualitative coding, and bilingual AI analysis.

## Architecture Overview

### Core Components

1. **Frontend**: Azure Static Web Apps (React)
2. **Backend API**: Azure App Service (FastAPI)
3. **Storage**: Azure Blob Storage (documents, audio)
4. **Database**: Azure SQL Database (metadata, codes, projects)
5. **Search**: Azure AI Search (RAG, semantic search)
6. **Authentication**: Azure AD / Entra ID
7. **AI Services**: Gemini AI (via API) + Claude (optional)

## Prerequisites

- Azure subscription
- Azure CLI installed
- Docker installed
- Node.js 18+
- Python 3.11+
- Google Gemini API key
- (Optional) Anthropic Claude API key

## Step 1: Create Azure Resources

### 1.1 Resource Group

```bash
az group create --name qda-app-rg --location eastus
```

### 1.2 Azure SQL Database

```bash
# Create SQL Server
az sql server create \
  --name qda-sql-server \
  --resource-group qda-app-rg \
  --location eastus \
  --admin-user adminuser \
  --admin-password <your-password>

# Create Database
az sql db create \
  --resource-group qda-app-rg \
  --server qda-sql-server \
  --name qda-db \
  --service-objective S0

# Configure firewall
az sql server firewall-rule create \
  --resource-group qda-app-rg \
  --server qda-sql-server \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### 1.3 Azure Blob Storage

```bash
az storage account create \
  --name qdastorageacct \
  --resource-group qda-app-rg \
  --location eastus \
  --sku Standard_LRS

# Create containers
az storage container create --name documents --account-name qdastorageacct
az storage container create --name audio --account-name qdastorageacct
az storage container create --name transcripts --account-name qdastorageacct
```

### 1.4 Azure AI Search

```bash
az search service create \
  --name qda-search-service \
  --resource-group qda-app-rg \
  --location eastus \
  --sku basic
```

### 1.5 Azure Container Registry

```bash
az acr create \
  --resource-group qda-app-rg \
  --name qdacontainerreg \
  --sku Basic

az acr login --name qdacontainerreg
```

## Step 2: Database Schema

Create these tables in Azure SQL:

```sql
-- Projects table
CREATE TABLE projects (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    created_by NVARCHAR(255),
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE()
);

-- Documents table
CREATE TABLE documents (
    id INT PRIMARY KEY IDENTITY(1,1),
    project_id INT FOREIGN KEY REFERENCES projects(id),
    name NVARCHAR(255) NOT NULL,
    language NVARCHAR(10),
    file_type NVARCHAR(50),
    blob_url NVARCHAR(500),
    content NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Codes table
CREATE TABLE codes (
    id INT PRIMARY KEY IDENTITY(1,1),
    project_id INT FOREIGN KEY REFERENCES projects(id),
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    color NVARCHAR(7),
    parent_code_id INT NULL,
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Quotations table
CREATE TABLE quotations (
    id INT PRIMARY KEY IDENTITY(1,1),
    document_id INT FOREIGN KEY REFERENCES documents(id),
    code_id INT FOREIGN KEY REFERENCES codes(id),
    text_content NVARCHAR(MAX),
    start_position INT,
    end_position INT,
    created_by NVARCHAR(255),
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Audio sessions table
CREATE TABLE audio_sessions (
    id INT PRIMARY KEY IDENTITY(1,1),
    project_id INT FOREIGN KEY REFERENCES projects(id),
    file_name NVARCHAR(255),
    blob_url NVARCHAR(500),
    transcript NVARCHAR(MAX),
    language NVARCHAR(10),
    duration_seconds INT,
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Templates table
CREATE TABLE analysis_templates (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    system_prompt NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETDATE()
);
```

## Step 3: Backend Deployment

### 3.1 Build and Push Docker Image

```bash
cd backend

# Build image
docker build -t qdacontainerreg.azurecr.io/qda-backend:latest .

# Push to ACR
docker push qdacontainerreg.azurecr.io/qda-backend:latest
```

### 3.2 Create App Service

```bash
az appservice plan create \
  --name qda-app-plan \
  --resource-group qda-app-rg \
  --is-linux \
  --sku B1

az webapp create \
  --resource-group qda-app-rg \
  --plan qda-app-plan \
  --name qda-backend-api \
  --deployment-container-image-name qdacontainerreg.azurecr.io/qda-backend:latest
```

### 3.3 Configure Environment Variables

```bash
az webapp config appsettings set \
  --resource-group qda-app-rg \
  --name qda-backend-api \
  --settings \
    GOOGLE_API_KEY="your-gemini-key" \
    AZURE_SQL_CONNECTION="<connection-string>" \
    AZURE_STORAGE_CONNECTION="<storage-connection>" \
    AZURE_SEARCH_ENDPOINT="<search-endpoint>" \
    AZURE_SEARCH_KEY="<search-key>"
```

## Step 4: Frontend Deployment

### 4.1 Build Frontend

```bash
cd frontend
npm install
npm run build
```

### 4.2 Deploy to Static Web Apps

```bash
az staticwebapp create \
  --name qda-frontend \
  --resource-group qda-app-rg \
  --source https://github.com/ellymulah/qda-bilingual-app \
  --location eastus \
  --branch main \
  --app-location "/frontend" \
  --output-location "dist"
```

## Step 5: Configure Azure AD Authentication

### 5.1 Register Application

```bash
az ad app create --display-name "QDA Bilingual App"
```

### 5.2 Configure App Service Authentication

1. Go to Azure Portal → App Service → Authentication
2. Add Microsoft Identity Provider
3. Configure redirect URLs
4. Enable token store

## Step 6: Azure AI Search Setup

### 6.1 Create Index for Documents

```json
{
  "name": "qda-documents-index",
  "fields": [
    {"name": "id", "type": "Edm.String", "key": true},
    {"name": "content", "type": "Edm.String", "searchable": true},
    {"name": "language", "type": "Edm.String", "filterable": true},
    {"name": "project_id", "type": "Edm.String", "filterable": true},
    {"name": "embedding", "type": "Collection(Edm.Single)", "searchable": true, "dimensions": 1536}
  ]
}
```

## Step 7: Enhanced Features Implementation

See the ENHANCEMENTS.md file for:
- Document management with PDF/Word upload
- Qualitative coding workspace
- RAG-powered chat
- Advanced audio analysis
- Bilingual UI with RTL support

## Monitoring and Logging

### Application Insights

```bash
az monitor app-insights component create \
  --app qda-app-insights \
  --location eastus \
  --resource-group qda-app-rg
```

## Security Checklist

- ✅ Enable HTTPS only
- ✅ Configure CORS properly
- ✅ Use Managed Identity for Azure resources
- ✅ Enable Azure AD authentication
- ✅ Encrypt data at rest
- ✅ Use Azure Key Vault for secrets
- ✅ Configure network security groups
- ✅ Enable audit logging

## Cost Optimization

- Use B1 tier for dev/test
- Scale up to P1V2+ for production
- Enable autoscaling
- Use reserved instances for savings
- Monitor with Azure Cost Management

## Next Steps

1. Review ENHANCEMENTS.md for full feature list
2. Test deployment with sample data
3. Configure backup and disaster recovery
4. Set up CI/CD pipeline
5. Conduct security assessment
