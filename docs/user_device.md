# UserDevice
UserDeviceはユーザー毎のデバイスを管理します。
あるユーザーが使っている端末を区別する必要がある場合に用いられます。
これが必要な理由はBank Payを用いたチャージを行う場合は端末を区別できることが要件としてあるためです。


<a name="create-user-device"></a>
## CreateUserDevice: ユーザーのデバイス登録
ユーザーのデバイスを新規に登録します

```typescript
const response: Response<UserDevice> = await client.send(new CreateUserDevice({
  user_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ユーザーID
  metadata: "{\"user_agent\": \"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0\"}" // ユーザーデバイスのメタデータ
}));
```



### Parameters
**`user_id`** 
  


```json
{
  "type": "string",
  "format": "uuid"
}
```

**`metadata`** 
  

ユーザーのデバイス用の情報をメタデータを保持するために用います。
例: 端末の固有情報やブラウザのUser-Agent


```json
{
  "type": "string",
  "format": "json"
}
```



成功したときは
[UserDevice](./responses.md#user-device)
を返します


---


<a name="get-user-device"></a>
## GetUserDevice: ユーザーのデバイスを取得
ユーザーのデバイスの情報を取得します

```typescript
const response: Response<UserDevice> = await client.send(new GetUserDevice({
  user_device_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // ユーザーデバイスID
}));
```



### Parameters
**`user_device_id`** 
  


```json
{
  "type": "string",
  "format": "uuid"
}
```



成功したときは
[UserDevice](./responses.md#user-device)
を返します


---


<a name="activate-user-device"></a>
## ActivateUserDevice: デバイスの有効化
指定のデバイスを有効化し、それ以外の同一ユーザーのデバイスを無効化します。


```typescript
const response: Response<UserDevice> = await client.send(new ActivateUserDevice({
  user_device_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // ユーザーデバイスID
}));
```



### Parameters
**`user_device_id`** 
  


```json
{
  "type": "string",
  "format": "uuid"
}
```



成功したときは
[UserDevice](./responses.md#user-device)
を返します


---


