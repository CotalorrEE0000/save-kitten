# Hash Table: Concept, Properties, and Usage

## 1. What is a Hash Table?

> A hash table is a data structure that implements an associative array abstract data type, which maps keys to values. It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found. The hash function converts the key into a hash code, which is then mapped to an index within the array bounds. Ideally, the hash function assigns each key to a unique bucket, but collisions—where multiple keys map to the same bucket—can occur and must be resolved.

>
> 哈希表是一种实现关联数组抽象数据类型的数据结构，能够将键映射到值。它使用哈希函数计算索引，指向桶或槽数组，从而找到所需的值。哈希函数将键转换为哈希码，再将其映射到数组范围内的索引。理想情况下，哈希函数为每个键分配唯一的桶，但可能会发生冲突——即多个键映射到同一个桶——必须加以解决。

## 2. Properties of a Hash Table

> Key properties of a hash table include: average-case time complexity of O(1) for insertion, deletion, and lookup operations, provided the hash function distributes keys uniformly; the ability to handle collisions through methods such as separate chaining (using linked lists) or open addressing; and the requirement of a good hash function to minimize collisions. The performance degrades to O(n) in the worst case when many collisions occur. Hash tables do not maintain order among elements, and their memory overhead includes the bucket array and collision resolution structures.

>
> 哈希表的主要特性包括：在哈希函数均匀分布键的前提下，插入、删除和查找操作的平均时间复杂度为 O(1)；能够通过链地址法（使用链表）或开放寻址法等方法处理冲突；需要良好的哈希函数以最小化冲突。当冲突频繁时，最坏情况性能会退化为 O(n)。哈希表不维护元素的顺序，其内存开销包括桶数组和冲突处理结构。

## 3. Using Hash Table in C++

> In C++, the Standard Library provides `std::unordered_map` (since C++11) as a hash table implementation. It is a template class requiring key and value types. Common operations include `insert` or `emplace` for adding elements, `find` for retrieving elements (returning an iterator), `erase` for removal, and `count` for checking existence. Iterators allow traversal, though order is not guaranteed. Example usage:
>
> ```cpp
> #include <unordered_map>
> #include <string>
> #include <iostream>
>
> int main() {
>     std::unordered_map<std::string, int> scores;
>     scores["Alice"] = 95;
>     scores.emplace("Bob", 87);
>     auto it = scores.find("Alice");
>     if (it != scores.end()) {
>         std::cout << it->second << std::endl;
>     }
>     scores.erase("Bob");
> }
> ```
>
> The hash function for standard types is built-in; for custom types, you must specialize `std::hash` or provide a custom hash function.

>
> 在 C++ 中，标准库提供了 `std::unordered_map`（自 C++11 起）作为哈希表实现。它是一个模板类，需要指定键和值的类型。常用操作包括：使用 `insert` 或 `emplace` 添加元素，`find` 查找元素（返回迭代器），`erase` 删除元素，`count` 检查是否存在。迭代器可用于遍历，但不保证顺序。用法示例：
>
> ```cpp
> #include <unordered_map>
> #include <string>
> #include <iostream>
>
> int main() {
>     std::unordered_map<std::string, int> scores;
>     scores["Alice"] = 95;
>     scores.emplace("Bob", 87);
>     auto it = scores.find("Alice");
>     if (it != scores.end()) {
>         std::cout << it->second << std::endl;
>     }
>     scores.erase("Bob");
> }
> ```
>
> 标准类型的哈希函数已内置；对于自定义类型，必须特化 `std::hash` 或提供自定义哈希函数。

## 4. C Language Implementation (Left Blank)

> In C, there is no built-in hash table container. To use a hash table, one must implement it manually using structures, dynamic memory allocation, and linked lists for collision handling. The implementation details, including the hash table structure definition, insertion, lookup, and destruction functions, are omitted here. A separate, ready-to-use C code file will be provided for practical integration.

>
> 在 C 语言中，没有内置的哈希表容器。要使用哈希表，必须使用结构体、动态内存分配和链表（处理冲突）手动实现。具体实现细节，包括哈希表结构体定义、插入、查找和销毁函数，此处留白。后续将提供一份开箱即用的 C 代码文件，供实际集成使用。