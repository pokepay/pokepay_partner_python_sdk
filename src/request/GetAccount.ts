// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { AccountDetail } from "../response/AccountDetail";

class GetAccount implements Request<AccountDetail> {
  public readonly __r: AccountDetail | undefined;
  public readonly method: Method = "GET";
  public readonly path: string;
  public readonly bodyParams: {};
  public constructor(params: {
    account_id: string
  }) {
    if (params.account_id === void 0) throw new Error('"account_id" is required');
    this.path = "/accounts" + "/" + params.account_id;
    this.bodyParams = {};
  }
}

export { GetAccount };