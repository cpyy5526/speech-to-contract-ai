const pathToClass = (path) => ({
  "gifted_property.type": "gift-type",
  "gifted_property.details": "gift-details",
  "delivery_details.delivery_date": "delivery-date",
  "delivery_details.delivery_method": "delivery-method",
  "rights_and_obligations.existing_rights": "gift-rights",
  "rights_and_obligations.obligations": "gift-obligations",
  "termination_conditions.reasons": "termination-reasons",
  "termination_conditions.procedure": "termination-procedure",
}[path]);

export default pathToClass;
