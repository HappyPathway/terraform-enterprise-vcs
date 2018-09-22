data "template_file" "vcs" {
  template = "${file("${path.module}/templates/create.json")}"

  vars {
    personal_access_token       = "${var.personal_access_token}"
    http_url      = "${var.http_url}"
    api_url = "${var.api_url}"
    service_provider = "${var.service_provider}"
  }
}

data "external" "module_publish" {
  program = ["python", "${path.module}/scripts/oauth_clients.py"]

  query = {
    vcs_config = "${data.template_file.vcs.rendered}"
    tfe_org       = "${var.tfe_org}"
    tfe_api = "${var.tfe_api}"
    tfe_token = "${var.tfe_token}"
  }
}
