// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { AccountWithUser } from "../response/AccountWithUser";

class CreateCustomerAccount implements Request<AccountWithUser> {
  public readonly __r: AccountWithUser | undefined;
  public readonly method: Method = "POST";
  public readonly path: string;
  public readonly bodyParams: {
    private_money_id: string,
    user_name?: string,
    account_name?: string,
    external_id?: string
  };
  public constructor(params: {
    private_money_id: string,
    user_name?: string,
    account_name?: string,
    external_id?: string
  }) {
    if (params.private_money_id === void 0) throw new Error('"private_money_id" is required');
    this.path = "/accounts" + "/customers";
    this.bodyParams = {
      private_money_id: params.private_money_id,
    };
    if (params.user_name !== void 0) this.bodyParams.user_name = params.user_name;
    if (params.account_name !== void 0) this.bodyParams.account_name = params.account_name;
    if (params.external_id !== void 0) this.bodyParams.external_id = params.external_id;
  }
}

export { CreateCustomerAccount };