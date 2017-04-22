# Thread学习

标签（空格分隔）： study

---

#### 条件变量
- 条件变量需要搭配互斥锁使用，在wait和notify前需要先获取（acquire）该锁，结束后需要释放（release）；
- wait阻塞的时候会先release取到的锁，当wait结束会恢复acquire状态。




