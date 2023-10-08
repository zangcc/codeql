import java

// 从所有的字段中选择
from Field field
// 过滤掉那些有注解的字段
where not exists(Annotation an | an.getAnnotatedElement() = field.getAnAnnotation())
// 输出字段的名称和位置
select field, field.getLocation()