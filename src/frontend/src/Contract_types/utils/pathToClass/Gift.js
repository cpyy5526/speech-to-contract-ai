const pathToClass = (path) => ({
  "contract-date": "contract-date",
  
  "gifted_property.type": "gift-type",
  "gifted_property.details": "gift-description",
  "delivery_details.delivery_date": "delivery-date",
  "delivery_details.delivery_method": "delivery-method",
  "rights_and_obligations.existing_rights": "existing-rights",
  "rights_and_obligations.obligations": "obligations",
  "termination_conditions.reasons": "termination-reasons",
  "termination_conditions.procedure": "termination-procedure",
}[path]);

export default pathToClass;
