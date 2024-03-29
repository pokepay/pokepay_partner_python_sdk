// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { Check } from "../response/Check";

class UpdateCheck implements Request<Check> {
  public readonly __r: Check | undefined;
  public readonly method: Method = "PATCH";
  public readonly path: string;
  public readonly bodyParams: {
    money_amount?: number,
    point_amount?: number,
    description?: string,
    is_onetime?: boolean,
    usage_limit?: number,
    expires_at?: string,
    point_expires_at?: string,
    point_expires_in_days?: number,
    bear_point_account?: string,
    is_disabled?: boolean
  };
  public constructor(params: {
    check_id: string,
    money_amount?: number,
    point_amount?: number,
    description?: string,
    is_onetime?: boolean,
    usage_limit?: number,
    expires_at?: string,
    point_expires_at?: string,
    point_expires_in_days?: number,
    bear_point_account?: string,
    is_disabled?: boolean
  }) {
    if (params.check_id === void 0) throw new Error('"check_id" is required');
    this.path = "/checks" + "/" + params.check_id;
    this.bodyParams = {};
    if (params.money_amount !== void 0) this.bodyParams.money_amount = params.money_amount;
    if (params.point_amount !== void 0) this.bodyParams.point_amount = params.point_amount;
    if (params.description !== void 0) this.bodyParams.description = params.description;
    if (params.is_onetime !== void 0) this.bodyParams.is_onetime = params.is_onetime;
    if (params.usage_limit !== void 0) this.bodyParams.usage_limit = params.usage_limit;
    if (params.expires_at !== void 0) this.bodyParams.expires_at = params.expires_at;
    if (params.point_expires_at !== void 0) this.bodyParams.point_expires_at = params.point_expires_at;
    if (params.point_expires_in_days !== void 0) this.bodyParams.point_expires_in_days = params.point_expires_in_days;
    if (params.bear_point_account !== void 0) this.bodyParams.bear_point_account = params.bear_point_account;
    if (params.is_disabled !== void 0) this.bodyParams.is_disabled = params.is_disabled;
  }
}

export { UpdateCheck };
