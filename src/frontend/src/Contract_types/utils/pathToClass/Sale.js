const pathToClass = (path) => ({
  "contract-date": "contract-date",
  
  "property.location": "property-location",

  "sale_price.total_price": "price-total",
  "sale_price.down_payment.amount": "price-down",
  "sale_price.down_payment.payment_date": "date-down",
  "sale_price.interim_payment.amount": "price-interim",
  "sale_price.interim_payment.payment_date": "date-interim",
  "sale_price.balance_payment.amount": "price-balance",
  "sale_price.balance_payment.payment_date": "date-balance",

  "ownership_transfer.document_transfer_date": "date-doc",
  "ownership_transfer.property_delivery_date": "date-delivery",

  "termination.penalty_amount": "penalty",
}[path]);

export default pathToClass;
