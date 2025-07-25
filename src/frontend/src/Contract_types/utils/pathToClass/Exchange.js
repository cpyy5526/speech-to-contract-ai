const pathToClass = (path) => ({
  "contract-date": "contract-date",
  
  "property_A.location": "propertyA-location",
  "property_B.location": "propertyB-location",

  "exchange_payment.total_price": "exchange-total",
  "exchange_payment.down_payment.amount": "exchange-down",
  "exchange_payment.down_payment.payment_date": "date-down",
  "exchange_payment.interim_payment.amount": "exchange-interim",
  "exchange_payment.interim_payment.payment_date": "date-interim",
  "exchange_payment.balance_payment.amount": "exchange-balance",
  "exchange_payment.balance_payment.payment_date": "date-balance",

  "ownership_transfer.document_transfer_date": "date-doc",
  "ownership_transfer.property_delivery_date": "date-delivery",

  "termination.penalty_amount": "penalty",

  "broker.office_name": "broker-office",
}[path]);

export default pathToClass;
