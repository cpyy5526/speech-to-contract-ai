const pathToClass = (path) => ({
  "property_A.location": "property-a-location",
  "property_B.location": "property-b-location",

  "exchange_payment.total_price": "price-total",
  "exchange_payment.down_payment.amount": "price-down",
  "exchange_payment.down_payment.payment_date": "date-down",
  "exchange_payment.interim_payment.amount": "price-interim",
  "exchange_payment.interim_payment.payment_date": "date-interim",
  "exchange_payment.balance_payment.amount": "price-balance",
  "exchange_payment.balance_payment.payment_date": "date-balance",

  "ownership_transfer.document_transfer_date": "date-doc",
  "ownership_transfer.property_delivery_date": "date-delivery",

  "termination.penalty_amount": "penalty",

  "broker.office_name": "agent-office",
}[path]);

export default pathToClass;
