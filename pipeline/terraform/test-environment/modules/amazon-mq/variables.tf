variable "environment" {
  type = string
  description = "A name for the environment to be used."
}
variable "security_group_id" {
  type = list(string)
  description = "The ID of the security group to use."
}