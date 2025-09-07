# How to Deploy Documentation to ReadTheDocs

This guide will walk you through deploying your WhatsApp SDK documentation to ReadTheDocs.

## Prerequisites

1. GitHub repository must be public or you need a ReadTheDocs Business account
2. Documentation files are already created in the `docs/` directory
3. `.readthedocs.yml` configuration file is in the repository root

## Step 1: Create ReadTheDocs Account

1. Go to https://readthedocs.org
2. Click "Sign Up"
3. Sign up using your GitHub account (recommended) or create a new account
4. Verify your email address

## Step 2: Import Your Project

1. Once logged in, click on your username → "My Projects"
2. Click "Import a Project"
3. If you connected GitHub, you'll see your repositories listed
4. Find `whatsapp-sdk-python` and click "+" to import it
5. Or manually import by clicking "Import Manually" and entering:
   - Name: `whatsapp-sdk`
   - Repository URL: `https://github.com/alejandrovelez243/whatsapp-sdk-python`
   - Repository type: Git
   - Default branch: main

## Step 3: Configure Project Settings

1. After import, go to your project dashboard
2. Click "Admin" → "Settings"
3. Configure:
   - **Name**: WhatsApp SDK Python
   - **Repository URL**: https://github.com/alejandrovelez243/whatsapp-sdk-python
   - **Default branch**: main
   - **Language**: English
   - **Programming Language**: Python
   - **Project homepage**: https://github.com/alejandrovelez243/whatsapp-sdk-python
   - **Tags**: whatsapp, sdk, python, api, meta

## Step 4: Configure Advanced Settings

1. Go to "Admin" → "Advanced Settings"
2. Set:
   - **Default version**: latest
   - **Privacy level**: Public
   - **Show version warning**: Yes (for development versions)
   - **Single version**: No (to support multiple versions)
   - **Python configuration file**: `.readthedocs.yml` (auto-detected)
   - **Requirements file**: `docs/requirements.txt` (auto-detected)

## Step 5: Build Documentation

1. Go to "Builds" tab
2. Click "Build Version" button
3. Select "latest" version
4. Click "Build"
5. Wait for the build to complete (usually 1-3 minutes)
6. Check build logs if there are any errors

## Step 6: View Your Documentation

Once the build succeeds:
1. Click "View Docs" button
2. Your documentation will be available at: https://whatsapp-sdk.readthedocs.io

## Step 7: Setup Webhook (Automatic Builds)

To automatically rebuild docs when you push to GitHub:

1. Go to "Admin" → "Integrations"
2. Click "Add integration"
3. Select "GitHub incoming webhook"
4. Copy the webhook URL
5. Go to your GitHub repository settings
6. Go to "Settings" → "Webhooks"
7. Click "Add webhook"
8. Paste the ReadTheDocs webhook URL
9. Set content type to `application/json`
10. Select "Just the push event"
11. Click "Add webhook"

Now documentation will automatically rebuild on every push to main branch.

## Step 8: Add Documentation Badge to README

Add this badge to your README.md:

```markdown
[![Documentation Status](https://readthedocs.org/projects/whatsapp-sdk/badge/?version=latest)](https://whatsapp-sdk.readthedocs.io/en/latest/?badge=latest)
```

## Step 9: Configure Custom Domain (Optional)

If you have a custom domain:

1. Go to "Admin" → "Domains"
2. Click "Add Domain"
3. Enter your domain (e.g., docs.yourproject.com)
4. Add the provided CNAME record to your DNS
5. Enable HTTPS

## Step 10: Version Management

To build documentation for specific versions:

1. Create a git tag: `git tag v1.0.0`
2. Push tag: `git push --tags`
3. Go to ReadTheDocs "Versions" tab
4. Activate the version you want to build
5. Click "Build" for that version

## Troubleshooting Common Issues

### Build Fails

1. Check build logs for specific errors
2. Common issues:
   - Missing dependencies in `docs/requirements.txt`
   - Syntax errors in RST files
   - Import errors in `conf.py`
   - Missing `__init__.py` files

### Documentation Not Updating

1. Check webhook is configured correctly
2. Verify branch name matches configuration
3. Manual trigger: Go to "Builds" → "Build Version"

### Sphinx Warnings

1. Check for broken internal links
2. Verify all referenced documents exist
3. Check RST syntax is correct

### Custom CSS/Theme Issues

1. Ensure theme is installed in `docs/requirements.txt`
2. Check `html_theme` in `conf.py`
3. Verify static files are in `docs/_static/`

## Local Testing

Before deploying, test documentation locally:

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Build documentation
cd docs
make html

# View in browser
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux
start _build/html/index.html  # Windows
```

## Additional Resources

- [ReadTheDocs Documentation](https://docs.readthedocs.io)
- [Sphinx Documentation](https://www.sphinx-doc.org)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [MyST Parser (Markdown support)](https://myst-parser.readthedocs.io)

## Support

If you encounter issues:
1. Check ReadTheDocs build logs
2. Search [ReadTheDocs GitHub Issues](https://github.com/readthedocs/readthedocs.org/issues)
3. Ask in [ReadTheDocs Community](https://readthedocs.org/support/)
4. Open issue in [whatsapp-sdk-python repository](https://github.com/alejandrovelez243/whatsapp-sdk-python/issues)
