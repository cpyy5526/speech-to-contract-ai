const pathToClass = (path) => ({
  "property.address": "property-address",

  "lease_terms.deposit": "lease-deposit",
  "lease_terms.monthly_rent": "lease-rent",
  "lease_terms.contract_period.start_date": "lease-start",
  "lease_terms.contract_period.end_date": "lease-end",
  "lease_terms.payment_date": "lease-payment",

  "management_fee": "management-fee",
  "delivery_date": "delivery-date",
  "termination": "termination",

  "real_estate_agent.office_name": "agent-office",
}[path]);

export default pathToClass;
