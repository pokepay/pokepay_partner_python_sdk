// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { Cashtray } from "../response/Cashtray";

class UpdateCashtray implements Request<Cashtray> {
  public readonly __r: Cashtray | undefined;
  public readonly method: Method = "PATCH";
  public readonly path: string;
  public readonly bodyParams: {
    amount?: number,
    description?: string,
    expires_in?: number
  };
  public constructor(params: {
    cashtray_id: string,
    amount?: number,
    description?: string,
    expires_in?: number
  }) {
    if (params.cashtray_id === void 0) throw new Error('"cashtray_id" is required');
    this.path = "/cashtrays" + "/" + params.cashtray_id;
    this.bodyParams = {};
    if (params.amount !== void 0) this.bodyParams.amount = params.amount;
    if (params.description !== void 0) this.bodyParams.description = params.description;
    if (params.expires_in !== void 0) this.bodyParams.expires_in = params.expires_in;
  }
}

export { UpdateCashtray };