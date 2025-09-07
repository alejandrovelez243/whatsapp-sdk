# Configuración de Despliegue Automático de Documentación

## 🚀 Configuración Inicial en ReadTheDocs

### Paso 1: Importar el Proyecto

1. Ve a https://readthedocs.org
2. Inicia sesión con tu cuenta de GitHub
3. Click en "Import a Project"
4. Busca `whatsapp-sdk` o `whatsapp-sdk-python`
5. Click en el botón "+" para importarlo

### Paso 2: Configuración Automática del Webhook

Cuando importas un proyecto desde GitHub, ReadTheDocs automáticamente:
- ✅ Crea un webhook en tu repositorio de GitHub
- ✅ Configura los permisos necesarios
- ✅ Activa el auto-build en cada push

### Paso 3: Verificar el Webhook

1. Ve a tu repositorio en GitHub: https://github.com/alejandrovelez243/whatsapp-sdk
2. Ve a Settings → Webhooks
3. Deberías ver un webhook de ReadTheDocs con:
   - **URL**: `https://readthedocs.org/api/v2/webhook/...`
   - **Events**: Push events
   - **Status**: ✅ Active

## 🔧 Configuración Avanzada (Opcional)

### Activar Build en Pull Requests

1. En ReadTheDocs, ve a tu proyecto
2. Admin → Advanced Settings
3. Activa "Build pull requests for this project"
4. Guarda cambios

Esto creará previews de documentación para cada PR.

### Configurar Versiones Automáticas

En `.readthedocs.yml` ya está configurado:

```yaml
version: 2
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
```

### Configurar Builds por Rama

1. En ReadTheDocs → Versions
2. Puedes activar builds para:
   - `main` (latest) - Ya activo por defecto
   - `stable` - Para versión estable
   - Tags (`v*`) - Para versiones específicas

## 📝 Flujo de Trabajo Automático

### Cuando haces cambios en documentación:

```bash
# 1. Editar documentación
vim docs/quickstart.rst

# 2. Commit y push
git add docs/
git commit -m "docs: update quickstart guide"
git push origin main

# 3. ¡AUTOMÁTICO! ReadTheDocs:
#    - Recibe webhook de GitHub
#    - Inicia build (~2-3 minutos)
#    - Actualiza https://whatsapp-sdk.readthedocs.io
```

### Para nuevas versiones:

```bash
# 1. Crear tag de versión
git tag v1.0.0
git push --tags

# 2. ¡AUTOMÁTICO! ReadTheDocs:
#    - Detecta nuevo tag
#    - Crea versión v1.0.0
#    - Disponible en: https://whatsapp-sdk.readthedocs.io/en/v1.0.0/
```

## 🔔 Notificaciones de Build

### Configurar notificaciones por email:

1. ReadTheDocs → Admin → Notifications
2. Activa notificaciones para:
   - ✅ Build failures
   - ⚠️ Build warnings (opcional)
   - ✅ Security updates

### Ver estado de builds:

1. En tu README.md ya tienes el badge:
   ```markdown
   [![Documentation Status](https://readthedocs.org/projects/whatsapp-sdk/badge/?version=latest)](https://whatsapp-sdk.readthedocs.io/en/latest/?badge=latest)
   ```

2. Dashboard de builds: https://readthedocs.org/projects/whatsapp-sdk/builds/

## 🐛 Troubleshooting

### Si los builds no se disparan automáticamente:

1. **Verificar webhook en GitHub**:
   ```bash
   # Ver webhooks recientes
   GitHub → Settings → Webhooks → Click on ReadTheDocs webhook → Recent Deliveries
   ```

2. **Verificar permisos**:
   - El webhook necesita permisos de `push` events
   - Tu cuenta de ReadTheDocs debe tener acceso al repo

3. **Forzar rebuild manual**:
   - ReadTheDocs → Builds → Build Version

### Si el build falla:

1. Ver logs completos en ReadTheDocs → Builds
2. Errores comunes:
   - Falta algún archivo en `docs/`
   - Error de sintaxis en RST
   - Dependencia faltante en `docs/requirements.txt`

## 🎯 Mejores Prácticas

1. **Test local antes de push**:
   ```bash
   cd docs
   make clean
   make html
   # Verificar que no hay errores
   ```

2. **Usar pre-commit hooks**:
   ```yaml
   # .pre-commit-config.yaml
   - repo: https://github.com/pre-commit/pygrep-hooks
     hooks:
       - id: rst-backticks
       - id: rst-directive-colons
       - id: rst-inline-touching-normal
   ```

3. **Versionado semántico**:
   - `latest` - Desarrollo activo (main branch)
   - `stable` - Última versión estable
   - `v1.0.0` - Versiones específicas

## 📊 Monitoreo

### Dashboard de ReadTheDocs

- **URL**: https://readthedocs.org/projects/whatsapp-sdk/
- **Métricas disponibles**:
  - Build history
  - Build times
  - Page views
  - Search analytics

### GitHub Actions para validación

Ya tienes CI que valida la documentación en cada PR:

```yaml
# .github/workflows/ci.yml
- name: Build documentation
  run: |
    cd docs
    make html
```

## ✅ Checklist de Configuración

- [ ] Proyecto importado en ReadTheDocs
- [ ] Webhook activo en GitHub
- [ ] Build automático funcionando
- [ ] Badge en README.md
- [ ] Notificaciones configuradas
- [ ] Primera versión publicada

## 🔗 Links Útiles

- **Tu documentación**: https://whatsapp-sdk.readthedocs.io
- **Panel de control**: https://readthedocs.org/projects/whatsapp-sdk/
- **Builds**: https://readthedocs.org/projects/whatsapp-sdk/builds/
- **Versiones**: https://readthedocs.org/projects/whatsapp-sdk/versions/
