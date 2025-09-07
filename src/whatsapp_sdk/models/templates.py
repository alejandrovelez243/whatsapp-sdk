"""
Template models for WhatsApp SDK.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field, field_validator

from whatsapp_sdk.models.base import BaseWhatsAppModel, ComponentType, ParameterType


class TemplateCategory(str, Enum):
    """Template categories."""

    AUTHENTICATION = "AUTHENTICATION"
    MARKETING = "MARKETING"
    UTILITY = "UTILITY"


class TemplateStatus(str, Enum):
    """Template status."""

    APPROVED = "APPROVED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    DISABLED = "DISABLED"
    IN_APPEAL = "IN_APPEAL"
    PENDING_DELETION = "PENDING_DELETION"
    DELETED = "DELETED"
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"
    PAUSED = "PAUSED"


class TemplateLanguage(str, Enum):
    """Template languages."""

    AF = "af"  # Afrikaans
    AR = "ar"  # Arabic
    BG = "bg"  # Bulgarian
    BN = "bn"  # Bengali
    CA = "ca"  # Catalan
    CS = "cs"  # Czech
    DA = "da"  # Danish
    DE = "de"  # German
    EL = "el"  # Greek
    EN = "en"  # English
    EN_GB = "en_GB"  # English (UK)
    EN_US = "en_US"  # English (US)
    ES = "es"  # Spanish
    ES_AR = "es_AR"  # Spanish (Argentina)
    ES_ES = "es_ES"  # Spanish (Spain)
    ES_MX = "es_MX"  # Spanish (Mexico)
    ET = "et"  # Estonian
    FA = "fa"  # Persian
    FI = "fi"  # Finnish
    FR = "fr"  # French
    GU = "gu"  # Gujarati
    HE = "he"  # Hebrew
    HI = "hi"  # Hindi
    HR = "hr"  # Croatian
    HU = "hu"  # Hungarian
    ID = "id"  # Indonesian
    IT = "it"  # Italian
    JA = "ja"  # Japanese
    KA = "ka"  # Georgian
    KK = "kk"  # Kazakh
    KN = "kn"  # Kannada
    KO = "ko"  # Korean
    LO = "lo"  # Lao
    LT = "lt"  # Lithuanian
    LV = "lv"  # Latvian
    MK = "mk"  # Macedonian
    ML = "ml"  # Malayalam
    MR = "mr"  # Marathi
    MS = "ms"  # Malay
    NB = "nb"  # Norwegian
    NL = "nl"  # Dutch
    PA = "pa"  # Punjabi
    PL = "pl"  # Polish
    PT_BR = "pt_BR"  # Portuguese (Brazil)
    PT_PT = "pt_PT"  # Portuguese (Portugal)
    RO = "ro"  # Romanian
    RU = "ru"  # Russian
    SK = "sk"  # Slovak
    SL = "sl"  # Slovenian
    SQ = "sq"  # Albanian
    SR = "sr"  # Serbian
    SV = "sv"  # Swedish
    SW = "sw"  # Swahili
    TA = "ta"  # Tamil
    TE = "te"  # Telugu
    TH = "th"  # Thai
    TR = "tr"  # Turkish
    UK = "uk"  # Ukrainian
    UR = "ur"  # Urdu
    UZ = "uz"  # Uzbek
    VI = "vi"  # Vietnamese
    ZH_CN = "zh_CN"  # Chinese (Simplified)
    ZH_HK = "zh_HK"  # Chinese (Hong Kong)
    ZH_TW = "zh_TW"  # Chinese (Traditional)


class TemplateParameter(BaseWhatsAppModel):
    """Template parameter model."""

    type: ParameterType = Field(..., description="Parameter type")
    text: Optional[str] = Field(None, description="Text parameter value")
    image: Optional[Dict[str, str]] = Field(None, description="Image parameter")
    video: Optional[Dict[str, str]] = Field(None, description="Video parameter")
    document: Optional[Dict[str, str]] = Field(None, description="Document parameter")
    currency: Optional[Dict[str, Any]] = Field(None, description="Currency parameter")
    date_time: Optional[Dict[str, Any]] = Field(None, description="Date time parameter")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: Optional[str]) -> Optional[str]:
        """Validate text parameter."""
        if v and len(v) > 32768:
            raise ValueError("Text parameter cannot exceed 32768 characters")
        return v


class TemplateComponent(BaseWhatsAppModel):
    """Template component model."""

    type: ComponentType = Field(..., description="Component type")
    parameters: List[TemplateParameter] = Field(default_factory=list, description="Parameters")
    sub_type: Optional[str] = Field(None, description="Component sub-type")
    index: Optional[int] = Field(None, description="Button index for button components")


class Template(BaseWhatsAppModel):
    """Template model."""

    name: str = Field(..., description="Template name")
    language: Dict[str, str] = Field(..., description="Template language")
    components: Optional[List[TemplateComponent]] = Field(
        None, description="Template components"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate template name."""
        if not v.strip():
            raise ValueError("Template name cannot be empty")
        if len(v) > 512:
            raise ValueError("Template name cannot exceed 512 characters")
        return v.lower()

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: Dict[str, str]) -> Dict[str, str]:
        """Validate language format."""
        if "code" not in v:
            raise ValueError("Language must have a code")
        return v


class Component(BaseWhatsAppModel):
    """Component for template creation."""

    type: ComponentType = Field(..., description="Component type")
    format: Optional[str] = Field(None, description="Component format (for headers)")
    text: Optional[str] = Field(None, description="Component text")
    example: Optional[Dict[str, Any]] = Field(None, description="Example values")
    buttons: Optional[List[Dict[str, Any]]] = Field(None, description="Button components")


class TemplateRequest(BaseWhatsAppModel):
    """Template creation request model."""

    name: str = Field(..., description="Template name")
    category: TemplateCategory = Field(..., description="Template category")
    language: str = Field(..., description="Template language")
    components: List[Component] = Field(..., description="Template components")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate template name."""
        # Template names must be lowercase with underscores
        if not v.strip():
            raise ValueError("Template name cannot be empty")
        if not v.replace("_", "").isalnum():
            raise ValueError("Template name can only contain letters, numbers, and underscores")
        if len(v) > 512:
            raise ValueError("Template name cannot exceed 512 characters")
        return v.lower()


class TemplateResponse(BaseWhatsAppModel):
    """Template response model."""

    id: str = Field(..., description="Template ID")
    status: TemplateStatus = Field(..., description="Template status")
    category: TemplateCategory = Field(..., description="Template category")
    name: Optional[str] = Field(None, description="Template name")
    language: Optional[str] = Field(None, description="Template language")
    components: Optional[List[Dict[str, Any]]] = Field(None, description="Template components")
    rejected_reason: Optional[str] = Field(None, description="Rejection reason if rejected")
    quality_score: Optional[Dict[str, Any]] = Field(None, description="Template quality score")
