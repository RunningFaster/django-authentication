from django.test import TestCase

# Create your tests here.


# def test_tree(self, request, *args, **kwargs):
#     res = {}
#     instance = TreeTest.objects.get(pk=7)
#     # 返回一个包含所有当前实例祖宗的queryset
#     ancetors = instance.get_ancestors(ascending=False, include_self=False)
#     res["ancetors"] = [i.name for i in ancetors]
#     # 返回包换当前实例的直接孩子的queryset(即下一级所有的子节点)，按树序排列
#     children = instance.get_children()
#     res["children"] = [i.name for i in children]
#     # 返回当前实例的所有子节点，按树序排列
#     descendants = instance.get_descendants(include_self=False)
#     res["descendants"] = [i.name for i in descendants]
#     family = instance.get_family()
#     res["family"] = [i.name for i in family]
#     return Response(res)
