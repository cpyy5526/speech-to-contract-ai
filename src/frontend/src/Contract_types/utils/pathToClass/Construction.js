const pathToClass = (path) => ({
  "contract_details.construction_name": "construction-name",
  "contract_details.construction_location": "construction-location",
  "contract_details.construction_period.start_date": "construction-start",
  "contract_details.construction_period.end_date": "construction-end",
  "contract_details.construction_scope": "construction-scope",

  "contract_amount.total_amount": "amount-total",
  "contract_amount.payment_method": "amount-method",
  "contract_amount.payment_schedule": "amount-schedule",

  "obligation_and_rights.ordering_party_obligation": "obligation-ordering",
  "obligation_and_rights.contractor_obligation": "obligation-contractor",

  "delay_penalty": "delay-penalty",
  "warranty_period": "warranty-period",
  "dispute_resolution": "dispute-resolution",
}[path]);

export default pathToClass;
