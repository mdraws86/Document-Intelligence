from typing import Optional, Any, List, Literal, Dict, TypedDict
from pydantic import BaseModel, Field
from langchain_core.runnables import Runnable

class ExtractInput(TypedDict):
    context: str

class Party(BaseModel):
    """Represent a contract party and its role.

    Attributes:
        name (Optional[str]): Legal entity name.
        role (Optional[str]): Role in the contract (e.g. customer, vendor).
        address (Optional[str]): Full address.
        country (Optional[str]): Country code or name.
    """
    name: Optional[str] = Field(default=None, description="Legal entity name")
    role: Optional[str] = Field(default=None, description="customer, vendor, licensor, etc.")
    address: Optional[str] = None
    country: Optional[str] = None


class CommercialTerms(BaseModel):
    """Represent key commercial terms of a contract.

    Attributes:
        amount_value (Optional[float]): Monetary value without currency symbol.
        amount_currency (Optional[str]): ISO 4217 currency code.
        billing_frequency (Optional[str]): Billing interval.
        taxes_included (Optional[bool]): Whether taxes are included.
        due_days (Optional[int]): Payment due period in days.
        late_fee (Optional[str]): Late fee description.
        late_interest (Optional[str]): Late interest description.
        payment_method (Optional[str]): Payment method.
    """
    amount_value: Optional[float] = Field(default=None, description="Number only, no currency symbol")
    amount_currency: Optional[str] = Field(default=None, description="ISO 4217 currency code, e.g. EUR, USD")
    billing_frequency: Optional[Literal["one_time", "monthly", "quarterly", "yearly", "per_usage", "other"]] = None
    taxes_included: Optional[bool] = None
    due_days: Optional[int] = None
    late_fee: Optional[str] = None
    late_interest: Optional[str] = None
    payment_method: Optional[str] = None


class Timeline(BaseModel):
    """Represent contract timeline and duration details.

    Attributes:
        effective_date (Optional[str]): Date the contract becomes effective.
        start_date (Optional[str]): Start date of obligations.
        end_date (Optional[str]): End or expiry date.
        term_months (Optional[int]): Contract duration in months.
        auto_renewal (Optional[bool]): Whether contract renews automatically.
        renewal_notice_days (Optional[int]): Notice period for renewal.
        termination_notice_days (Optional[int]): Notice period for termination.
    """
    effective_date: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    term_months: Optional[int] = None
    auto_renewal: Optional[bool] = None
    renewal_notice_days: Optional[int] = None
    termination_notice_days: Optional[int] = None


class LegalTerms(BaseModel):
    """Represent key legal clauses of a contract.

    Attributes:
        governing_law (Optional[str]): Applicable law.
        jurisdiction (Optional[str]): Legal venue for disputes.
        confidentiality (Optional[bool]): Confidentiality clause present.
        data_protection (Optional[bool]): Data protection clause present.
        indemnification (Optional[bool]): Indemnification clause present.
        limitation_of_liability (Optional[bool]): Liability limitation clause.
        ip_ownership (Optional[str]): Intellectual property ownership.
        exclusivity (Optional[bool]): Exclusivity clause present.
        assignment_restrictions (Optional[bool]): Assignment restrictions.
        force_majeure (Optional[bool]): Force majeure clause present.
    """
    governing_law: Optional[str] = None
    jurisdiction: Optional[str] = None
    confidentiality: Optional[bool] = None
    data_protection: Optional[bool] = None
    indemnification: Optional[bool] = None
    limitation_of_liability: Optional[bool] = None
    ip_ownership: Optional[str] = None
    exclusivity: Optional[bool] = None
    assignment_restrictions: Optional[bool] = None
    force_majeure: Optional[bool] = None


class ContractExtraction(BaseModel):
    """Structured representation of extracted contract data.

    Attributes:
        file_name (Optional[str]): Source file name.
        contract_title (Optional[str]): Title of the contract.
        contract_type (Optional[str]): Type (e.g. NDA, lease, loan).
        language (Optional[str]): Document language.
        parties (List[Party]): Involved parties.
        commercial_terms (CommercialTerms): Financial terms.
        timeline (Timeline): Duration and dates.
        legal_terms (LegalTerms): Legal clauses.
        scope_summary (Optional[str]): Summary of contract scope.
        services_or_deliverables (List[str]): Services or deliverables.
        obligations_customer (List[str]): Customer obligations.
        obligations_vendor (List[str]): Vendor obligations.
        sla_or_support (Optional[str]): SLA or support terms.
        penalty_or_breach_clauses (List[str]): Penalties and breach clauses.
        risk_flags (List[str]): Identified risks.
        signature_date (Optional[str]): Signing date.
        signed_by (List[str]): Signing parties.
        evidence_quotes (List[str]): Supporting text excerpts.
        confidence (Optional[float]): Extraction confidence (0–1).
    """
    file_name: Optional[str] = None
    contract_title: Optional[str] = None
    contract_type: Optional[str] = None
    language: Optional[str] = None

    parties: List[Party] = Field(default_factory=list)

    commercial_terms: CommercialTerms = Field(default_factory=CommercialTerms)
    timeline: Timeline = Field(default_factory=Timeline)
    legal_terms: LegalTerms = Field(default_factory=LegalTerms)

    scope_summary: Optional[str] = None
    services_or_deliverables: List[str] = Field(default_factory=list)
    obligations_customer: List[str] = Field(default_factory=list)
    obligations_vendor: List[str] = Field(default_factory=list)
    sla_or_support: Optional[str] = None

    penalty_or_breach_clauses: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)

    signature_date: Optional[str] = None
    signed_by: List[str] = Field(default_factory=list)

    evidence_quotes: List[str] = Field(default_factory=list)
    confidence: Optional[float] = Field(default=None, ge=0, le=1)

def extract_contract_data(
    context: str,
    extract_chain: Runnable[ExtractInput, ContractExtraction],
    file_name: str | None = None
    ) -> Dict[str, Any]:
    """Extract structured contract data from text using an LLM chain.

    Input:
        context (str): Preprocessed contract text used as model input.
        extract_chain: LLM extraction chain with structured output.
        file_name (Optional[str]): Optional file name to attach to result.

    Output:
        Dict[str, Any]: Extracted contract data as a dictionary.
    """
    # Invoke the LLM chain with the contract context
    result = extract_chain.invoke({"context": context})

    # Convert Pydantic output model to a dictionary
    data = result.model_dump()

    # Ensure confidence is within 0–1 range
    if data.get("confidence") is not None:
        data["confidence"] = max(0, min(1, data["confidence"]))

    # Attach file name if provided
    if file_name:
        data["file_name"] = file_name

    # Return the extracted contract data as a dictionary
    return data