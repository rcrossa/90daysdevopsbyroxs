# infrastructure-calculator/main.tf
variable "instances" {
  type = map(object({
    count = number
    type  = string
    hours = number
  }))
}

locals {
  # Precios por hora (ejemplo)
  pricing = {
    "t3.micro"  = 0.0104
    "t3.small"  = 0.0208
    "t3.medium" = 0.0416
    "t3.large"  = 0.0832
  }

  # Calcular costos
  costs = {
    for name, config in var.instances :
    name => config.count * config.hours * local.pricing[config.type]
  }

  total_cost = sum(values(local.costs))
}

resource "local_file" "cost_report" {
  filename = "cost-report.json"
  content = jsonencode({
    instances    = var.instances
    costs        = local.costs
    total_cost   = local.total_cost
    currency     = "USD"
    generated_at = timestamp()
  })
}