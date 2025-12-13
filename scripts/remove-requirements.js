/**
 * Build script to remove requirements.txt before Vercel build
 * This prevents Vercel from installing heavy Python dependencies
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootRequirements = path.join(__dirname, '..', 'requirements.txt');
const backendRequirements = path.join(__dirname, '..', 'requirements-backend-only.txt');

console.log('🔧 Pre-build: Removing requirements.txt files...');

// Remove root requirements.txt if it exists
if (fs.existsSync(rootRequirements)) {
  fs.unlinkSync(rootRequirements);
  console.log('✅ Removed root requirements.txt');
}

// Remove requirements-backend-only.txt if it exists (Vercel might read it)
if (fs.existsSync(backendRequirements)) {
  fs.unlinkSync(backendRequirements);
  console.log('✅ Removed requirements-backend-only.txt');
}

// Ensure api/requirements.txt is empty
const apiRequirements = path.join(__dirname, '..', 'api', 'requirements.txt');
if (fs.existsSync(apiRequirements)) {
  const content = fs.readFileSync(apiRequirements, 'utf8');
  if (content.trim() && !content.includes('# Empty') && !content.includes('# No dependencies')) {
    // File has dependencies, make it empty
    fs.writeFileSync(apiRequirements, '# Empty - No dependencies\n# Serverless functions use pure Python standard library only\n');
    console.log('✅ Cleared api/requirements.txt');
  } else {
    console.log('✅ api/requirements.txt is already empty');
  }
} else {
  // Create empty api/requirements.txt
  const apiDir = path.join(__dirname, '..', 'api');
  if (!fs.existsSync(apiDir)) {
    fs.mkdirSync(apiDir, { recursive: true });
  }
  fs.writeFileSync(apiRequirements, '# Empty - No dependencies\n# Serverless functions use pure Python standard library only\n');
  console.log('✅ Created empty api/requirements.txt');
}

console.log('✅ Pre-build cleanup complete!');
