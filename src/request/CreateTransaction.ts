// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { TransactionDetail } from "../response/TransactionDetail";

class CreateTransaction implements Request<TransactionDetail> {
  public readonly __r: TransactionDetail | undefined;
  public readonly method: Method = "POST";
  public readonly path: string;
  public readonly bodyParams: {
    shop_id: string,
    customer_id: string,
    private_money_id: string,
    money_amount?: number,
    point_amount?: number,
    point_expires_at?: string,
    description?: string
  };
  public constructor(params: {
    shop_id: string,
    customer_id: string,
    private_money_id: string,
    money_amount?: number,
    point_amount?: number,
    point_expires_at?: string,
    description?: string
  }) {
    if (params.shop_id === void 0) throw new Error('"shop_id" is required');
    if (params.customer_id === void 0) throw new Error('"customer_id" is required');
    if (params.private_money_id === void 0) throw new Error('"private_money_id" is required');
    this.path = "/transactions";
    this.bodyParams = {
      shop_id: params.shop_id,
      customer_id: params.customer_id,
      private_money_id: params.private_money_id,
    };
    if (params.money_amount !== void 0) this.bodyParams.money_amount = params.money_amount;
    if (params.point_amount !== void 0) this.bodyParams.point_amount = params.point_amount;
    if (params.point_expires_at !== void 0) this.bodyParams.point_expires_at = params.point_expires_at;
    if (params.description !== void 0) this.bodyParams.description = params.description;
  }
}

export { CreateTransaction };
