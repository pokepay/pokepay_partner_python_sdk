// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { ShopWithAccounts } from "../response/ShopWithAccounts";

class GetShop implements Request<ShopWithAccounts> {
  public readonly __r: ShopWithAccounts | undefined;
  public readonly method: Method = "GET";
  public readonly path: string;
  public readonly bodyParams: {};
  public constructor(params: {
    shop_id: string
  }) {
    if (params.shop_id === void 0) throw new Error('"shop_id" is required');
    this.path = "/shops" + "/" + params.shop_id;
    this.bodyParams = {};
  }
}

export { GetShop };