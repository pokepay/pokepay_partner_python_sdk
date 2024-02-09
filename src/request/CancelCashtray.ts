// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { Cashtray } from "../response/Cashtray";

class CancelCashtray implements Request<Cashtray> {
  public readonly __r: Cashtray | undefined;
  public readonly method: Method = "DELETE";
  public readonly path: string;
  public readonly bodyParams: {};
  public constructor(params: {
    cashtray_id: string
  }) {
    if (params.cashtray_id === void 0) throw new Error('"cashtray_id" is required');
    this.path = "/cashtrays" + "/" + params.cashtray_id;
    this.bodyParams = {};
  }
}

export { CancelCashtray };