const pathToClass = (path) => ({
  "contract-date": "contract-date",
  
  "subject_property.name": "property-name",

  "loan_period.start_date": "loan-start",
  "loan_period.end_date": "loan-end",

  "compensation_for_damage": "compensation-damage",
  "restoration_obligation": "restoration-obligation",
}[path]);

export default pathToClass;
