# User

<a name="get-user"></a>
## GetUser

```typescript
const response: Response<AdminUserWithShopsAndPrivateMoneys> = await client.send(new GetUser());
```






成功したときは
[AdminUserWithShopsAndPrivateMoneys](./responses.md#admin-user-with-shops-and-private-moneys)
を返します

### Error Responses
|status|type|ja|en|
|---|---|---|---|
|403|unpermitted_admin_user|この管理ユーザには権限がありません|Admin does not have permission|



---



