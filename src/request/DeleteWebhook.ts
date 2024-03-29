// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { OrganizationWorkerTaskWebhook } from "../response/OrganizationWorkerTaskWebhook";

class DeleteWebhook implements Request<OrganizationWorkerTaskWebhook> {
  public readonly __r: OrganizationWorkerTaskWebhook | undefined;
  public readonly method: Method = "DELETE";
  public readonly path: string;
  public readonly bodyParams: {};
  public constructor(params: {
    webhook_id: string
  }) {
    if (params.webhook_id === void 0) throw new Error('"webhook_id" is required');
    this.path = "/webhooks" + "/" + params.webhook_id;
    this.bodyParams = {};
  }
}

export { DeleteWebhook };
